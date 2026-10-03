"""Client for `omp auth-gateway stdio`.

Protocol: one JSON line per request on stdin, one JSON line per reply on stdout,
matched by id. A single process answers requests one at a time (observed), so
GatewayPool runs several processes for parallelism.
"""
import collections
import json
import subprocess
import threading
import time
import uuid
from concurrent.futures import Future, TimeoutError as FutureTimeout

CHAT_PATH = "/v1/chat/completions"


class GatewayError(RuntimeError):
    pass


class Gateway:
    """One gateway process. Thread-safe; replies are demuxed by id, so order does not matter."""

    def __init__(self, cmd=("omp", "auth-gateway", "stdio"), retries=3, backoff=2.0, timeout=600.0):
        self.cmd = list(cmd)
        self.retries = retries
        self.backoff = backoff
        self.timeout = timeout
        self._lock = threading.Lock()  # guards proc, pending, stdin writes
        self._pending: dict[str, tuple] = {}  # id -> (proc, Future)
        self._proc = None
        self._stderr_tail = collections.deque(maxlen=20)
        self.inflight = 0

    # -- process management -------------------------------------------------
    def _start(self):
        proc = subprocess.Popen(
            self.cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        ready = proc.stdout.readline()
        try:
            ok = json.loads(ready).get("ready") is True
        except (ValueError, AttributeError):
            ok = False
        if not ok:
            proc.kill()
            raise GatewayError(f"gateway did not report ready: {ready!r}")
        threading.Thread(target=self._read_stdout, args=(proc,), daemon=True).start()
        threading.Thread(target=self._drain_stderr, args=(proc,), daemon=True).start()
        self._proc = proc

    def _drain_stderr(self, proc):
        for line in proc.stderr:
            self._stderr_tail.append(line.rstrip())

    def _read_stdout(self, proc):
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except ValueError:
                continue
            with self._lock:
                entry = self._pending.pop(msg.get("id"), None)
            fut = entry[1] if entry else None
            if fut is not None and not fut.done():
                fut.set_result(msg)
        # EOF: fail everything still waiting on this process
        with self._lock:
            if self._proc is proc:
                self._proc = None
            dead = [rid for rid, (p, _) in self._pending.items() if p is proc]
            failed = [self._pending.pop(rid)[1] for rid in dead]
        for fut in failed:
            if not fut.done():
                fut.set_exception(GatewayError("gateway process exited: " + " | ".join(self._stderr_tail)))

    def close(self):
        with self._lock:
            proc, self._proc = self._proc, None
        if proc is not None:
            try:
                proc.stdin.close()
                proc.wait(timeout=5)
            except Exception:
                proc.kill()

    # -- requests -----------------------------------------------------------
    def _request(self, path, body, timeout):
        rid = str(uuid.uuid4())
        fut: Future = Future()
        with self._lock:
            if self._proc is None:
                self._start()
            self._pending[rid] = (self._proc, fut)
            try:
                self._proc.stdin.write(json.dumps({"id": rid, "path": path, "body": body}) + "\n")
                self._proc.stdin.flush()
            except (BrokenPipeError, OSError) as e:
                self._pending.pop(rid, None)
                self._proc = None
                raise GatewayError(f"write failed: {e}")
        try:
            return fut.result(timeout=timeout)
        except FutureTimeout:
            with self._lock:
                self._pending.pop(rid, None)
            raise GatewayError(f"timeout after {timeout}s")

    def chat(self, model, messages, reasoning_effort=None, timeout=None):
        """-> {text, usage:{input_tokens,output_tokens,reasoning_tokens|None}, latency_ms}"""
        body = {"model": model, "messages": messages, "stream": False}
        if reasoning_effort:
            body["reasoning_effort"] = reasoning_effort
        timeout = timeout or self.timeout
        last = None
        for attempt in range(self.retries + 1):
            if attempt:
                time.sleep(self.backoff * 2 ** (attempt - 1))
            t0 = time.monotonic()
            try:
                reply = self._request(CHAT_PATH, body, timeout)
            except GatewayError as e:
                last = str(e)
                continue
            latency_ms = int((time.monotonic() - t0) * 1000)
            if reply.get("status") != 200:
                last = f"status {reply.get('status')}: {json.dumps(reply.get('body'))[:500]}"
                continue
            rbody = reply.get("body") or {}
            try:
                text = rbody["choices"][0]["message"]["content"]
            except (KeyError, IndexError, TypeError):
                last = f"malformed reply: {json.dumps(rbody)[:500]}"
                continue
            if not text or not text.strip():
                last = "empty content"
                continue
            usage = rbody.get("usage") or {}
            details = usage.get("completion_tokens_details") or {}
            return {
                "text": text,
                "usage": {
                    "input_tokens": usage.get("prompt_tokens"),
                    "output_tokens": usage.get("completion_tokens"),
                    "reasoning_tokens": details.get("reasoning_tokens"),
                },
                "latency_ms": latency_ms,
            }
        raise GatewayError(f"{model}: failed after {self.retries + 1} attempts: {last}")


class GatewayPool:
    """N gateway processes; each chat() goes to the least busy one."""

    def __init__(self, size=4, **kw):
        self._gws = [Gateway(**kw) for _ in range(size)]
        self._lock = threading.Lock()

    def chat(self, model, messages, reasoning_effort=None, timeout=None):
        with self._lock:
            gw = min(self._gws, key=lambda g: g.inflight)
            gw.inflight += 1  # reserve; chat() adds its own, released below
        try:
            return gw.chat(model, messages, reasoning_effort, timeout)
        finally:
            with self._lock:
                gw.inflight -= 1

    def close(self):
        for g in self._gws:
            g.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()
