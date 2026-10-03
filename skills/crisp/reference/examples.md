# CRISP before/after examples

### Software engineering explanation

*Prompt: "Why should I use a connection pool instead of opening a database connection per request?"*

**Before**
> Great question! Connection pooling is a crucial technique in modern application development, and understanding why it matters can significantly improve the performance and reliability of your applications.
>
> In essence, opening a new database connection for every request is an expensive operation. Each new connection requires a TCP handshake, TLS negotiation, and authentication, which can add anywhere from a few milliseconds to tens of milliseconds of latency. Additionally, databases typically limit the number of concurrent connections they can handle (PostgreSQL defaults to 100), so under heavy load you may exhaust the available connections and cause errors.
>
> A connection pool addresses these challenges by maintaining a set of reusable connections. When a request needs the database, it borrows a connection from the pool and returns it when done, which eliminates the setup cost and caps the total number of connections.
>
> In summary, connection pooling improves performance, protects your database from overload, and makes your application more scalable. I hope this helps! Let me know if you'd like me to go into more detail about pool sizing.

**CRISP**
> Because opening a connection is slow and databases cap them. Each new connection costs a TCP handshake, TLS negotiation, and authentication, which adds a few to tens of milliseconds. PostgreSQL also defaults to 100 concurrent connections, so without a pool a traffic spike exhausts them and requests fail. A pool opens connections once, lends one per request, and caps the total.

Words: 174 → 61 (−65%). Removed: praise opener, summary, offer of more, filler.

### Coding-agent task spec

*Situation: a planning model hands a coding agent its task.*

**Before**
> Hello! I'd like you to help me with an important task in our codebase. We have a payments service, and I'd like you to take a look at the payment client in `src/payments/client.py` and add some appropriate retry logic so that it's more robust when things go wrong. It would be great if you could handle errors properly and use a reasonable number of retries, perhaps around 3, with some kind of exponential backoff starting at about 200 ms. It's crucial that we don't retry in situations where it could cause a duplicate charge, so only requests that carry an idempotency key should be retried. Timeouts and 5xx responses are generally the cases worth retrying, whereas 4xx responses shouldn't be. Please also be careful not to break any existing functionality, and feel free to add tests if you think that would be helpful. Let me know if you have any questions or need clarification, and please provide a summary of the changes when you're done. Thank you so much for your help with this!

**CRISP**
> Add retries to the payment client in `src/payments/client.py`:
>
> - Retry only requests that carry an idempotency key, so a retry can't double-charge.
> - Retry on timeouts and 5xx responses. Never retry 4xx.
> - Make at most 3 retries, with exponential backoff starting at 200 ms.
> - Add a test for each rule.
>
> Done when the existing payment tests still pass and the new tests pass. Reply with a summary of the changes.

Words: 174 → 72 (−59%). Removed: greeting, vague qualifiers, ceremony, thanks.

### Coding-agent reply

*Situation: an agent reports back after fixing a session bug.*

**Before**
> I've successfully completed the task! Let me walk you through what I did. First, I carefully analyzed the codebase to understand the structure of the authentication module. After a thorough investigation, I discovered that the issue was caused by the token expiry check in `auth/session.py` comparing a timestamp in seconds against one in milliseconds, which meant tokens were being treated as valid long after they had expired. To fix this, I updated the comparison to convert both values to seconds. I also added a regression test in `tests/test_session.py` that covers the expired-token case. I then ran the full test suite, and all 214 tests pass. Additionally, it's worth noting that I noticed the same pattern in `auth/refresh.py`, but I did not change it since it was outside the scope of the task. You may want to take a look at it. In summary, the bug has been fixed, a test has been added, and everything is passing. Please let me know if you'd like me to make any further changes or if you have any questions!

**CRISP**
> Fixed: expired tokens passed the check in `auth/session.py` because it compared seconds against milliseconds. Both values are now in seconds. I added a regression test in `tests/test_session.py`; all 214 tests pass. I did not touch `auth/refresh.py`, which has the same pattern and is worth a look.

Words: 176 → 46 (−74%). Removed: narrated process, summary, closing offer, filler.

Kept: the `auth/refresh.py` risk. It is out of scope but it is the one thing the reader must act on next.

### Debugging answer

*Prompt: "My React component re-renders forever when I fetch data in useEffect. What's wrong?"*

**Before**
> Great question! Infinite re-render loops are a common issue that many React developers encounter, and there are a number of potential causes. Let's break this down.
>
> **Possible causes:**
> - **Missing dependency array:** If you don't pass a dependency array to `useEffect`, the effect runs after every render.
> - **State updates inside the effect:** Calling `setState` inside an effect that runs on every render triggers another render.
> - **Unstable dependencies:** Objects or functions created inline in the component body change identity on every render.
>
> **Recommended fixes:**
> - Add a dependency array, e.g. `useEffect(() => {...}, [])`.
> - Memoize objects and functions with `useMemo` and `useCallback`.
> - Make sure you're not mutating state directly.
>
> In most cases, the first one is the culprit. It's also worth noting that you should always consider adding cleanup functions to avoid memory leaks. I hope this helps! If you share your code, I'd be happy to take a closer look.

**CRISP**
> Most likely your effect has no dependency array, so it runs after every render, and its `setState` triggers the next render.
>
> 1. Check the `useEffect` call. If it has no second argument, add one: `useEffect(() => {...}, [])`.
> 2. If it already has an array and still loops, look for an object or function in it that is created inline in the component body. It gets a new identity on every render.
> 3. Wrap that value in `useMemo` or `useCallback`.

Words: 154 → 80 (−48%). Removed: praise opener, generic cause list, unrelated advice, closer.

### System design recommendation

*Prompt: "We're 3 engineers with a 40k-line app, 2,000 requests a minute, and one Postgres database. Should we split into microservices?"*

**Before**
> That's an excellent and important architectural question! The decision between a monolith and microservices depends on a variety of factors, and there are trade-offs to consider on both sides.
>
> Microservices offer several advantages, including independent deployability, technology flexibility, and the ability to scale individual components. However, they also introduce significant complexity, such as network latency, distributed transactions, service discovery, and the need for robust observability and CI/CD pipelines.
>
> Given that you have a team of three engineers, a codebase of roughly 40,000 lines, and a modest traffic of about 2,000 requests per minute against a single Postgres database, it would generally be advisable to stay with your monolith for now. A well-structured modular monolith can provide many of the benefits of microservices without the operational overhead. You could consider extracting a service later if a specific component has distinct scaling needs or if the team grows to more than about 10 engineers.
>
> In conclusion, I would recommend keeping the monolith and focusing on modularity. Of course, the best choice depends on your specific circumstances, so feel free to share more details!

**CRISP**
> No, keep the monolith. At 3 engineers, 40k lines, and 2,000 requests a minute on one Postgres, microservices add network latency, distributed transactions, and deployment overhead, and solve no problem you have. Split the code into modules with clear boundaries instead. Extract a service only if one component needs to scale differently from the rest, or if the team passes about 10 engineers.

Words: 181 → 63 (−65%). Removed: praise opener, restated context, conclusion, generic trade-offs.

### Everyday question

*Prompt: "How long can I keep cooked rice in the fridge?"*

**Before**
> Great question! Food safety is really important, and cooked rice is one of those foods that requires some special care. Cooked rice can contain spores of a bacterium called Bacillus cereus, which can survive cooking and multiply at room temperature, potentially causing food poisoning.
>
> In general, cooked rice can be safely stored in the refrigerator for about 3 to 4 days, although many experts recommend consuming it within 1 to 2 days for the best quality and safety. To minimize risk, it's important to cool the rice as quickly as possible, ideally within an hour of cooking, and to store it in an airtight container in the refrigerator at 40°F (4°C) or below. When reheating, make sure the rice is steaming hot all the way through, and avoid reheating it more than once.
>
> If you're unsure whether your rice is still good, it's best to err on the side of caution. Please note that I'm not a food safety professional, and you should consult official guidelines for more information. I hope this helps!

**CRISP**
> 3 to 4 days, but it's best within 1 to 2. Cool it within an hour of cooking and keep it in an airtight container at 4°C (40°F) or below, because *Bacillus cereus* spores survive cooking and multiply at room temperature. Reheat it once only, until steaming hot throughout. If you can't tell how long it has been in there, throw it out.

Words: 173 → 63 (−64%). Removed: praise opener, disclaimer, vague attribution, closer.

### Technical explanation

*Prompt: "How does a TLS handshake work?"*

**Before**
> Great question! The TLS handshake is a fundamental part of how secure communication works on the internet, and understanding it is crucial for any developer. Let's dive into how it works.
>
> The TLS handshake is the process by which a client and a server establish a secure connection. Here's a comprehensive breakdown of the steps in TLS 1.3:
>
> **Step 1: Client Hello.** The client initiates the process by sending a message that includes the supported TLS versions, cipher suites, and a key share.
>
> **Step 2: Server Hello.** The server responds by choosing a cipher suite and sending its own key share.
>
> **Step 3: Key Derivation.** Both sides use the key shares to compute the same shared secret and derive the handshake keys. Encrypted under those keys, the server then sends its certificate and a signature proving it owns the certificate's private key.
>
> **Step 4: Finished.** Both sides send a Finished message to verify the handshake wasn't tampered with, after which encrypted application data begins to flow.
>
> It's worth noting that TLS 1.3 completes this in just one round trip, which is a significant improvement over TLS 1.2, which required two. In summary, the TLS handshake allows the client and server to agree on encryption parameters and authenticate the server. I hope this clarifies things!

**CRISP**
> A TLS 1.3 handshake agrees on encryption and authenticates the server in one round trip. TLS 1.2 needed two.
>
> 1. The client sends its supported TLS versions, cipher suites, and a key share.
> 2. The server picks a cipher suite and replies with its key share.
> 3. Both sides derive handshake keys from the key shares. Under those keys, the server sends its certificate and a signature proving it holds the certificate's private key.
> 4. Both send a Finished message that verifies the handshake wasn't tampered with. Encrypted application data starts after that.

Words: 214 → 93 (−57%). Removed: praise opener, step titles, summary, closer.

### Recommendation or comparison

*Prompt: "Which Python HTTP client should I use: requests, httpx, or aiohttp?"*

**Before**
> Great question! Choosing the right HTTP client library for Python is an important decision, and there are several excellent options available, each with their own strengths and weaknesses. Let me give you a comprehensive overview of the three most popular choices.
>
> **Requests** is arguably the most widely used HTTP library in the Python ecosystem. It boasts a simple, elegant API and a vast community. However, it only supports synchronous requests, which can be a limitation for high-concurrency applications.
>
> **HTTPX** is a modern, fully featured HTTP client that supports both synchronous and asynchronous requests. It offers an API that is largely compatible with Requests, and it also supports HTTP/2.
>
> **aiohttp** is a robust asynchronous library that serves as both an HTTP client and server. It's a great choice for async-first applications, but it does not offer a synchronous API.
>
> Ultimately, the best choice depends on your specific needs. If you only need synchronous calls, Requests is a solid choice. If you need both sync and async, HTTPX is a great option. If you're building an async-only application or need a server, aiohttp may be the way to go. I hope this helps you make an informed decision!

**CRISP**
> Use requests for sync only, httpx for sync and async, aiohttp for async only or when you also need an HTTP server.
>
> | Library | Sync | Async | Also |
> |---|---|---|---|
> | requests | yes | no | largest community |
> | httpx | yes | yes | requests-like API, HTTP/2 |
> | aiohttp | no | yes | includes an HTTP server |

Words: 196 → 65 (−67%). Removed: praise opener, prose duplicating facts, filler adjectives, closer.

### Status update to a team lead

*Situation: weekly update to Sarah on the invoice export project.*

**Before**
> Hi Sarah, I hope you're doing well! I wanted to take a moment to provide you with a comprehensive update on the progress of the invoice export project. Overall, things are going well and we're making steady progress. This week, the team has been working hard on several important items. We completed the CSV export endpoint and it's now deployed to staging. We also made some progress on the PDF export, which is about 60% done. Unfortunately, we've run into a bit of a challenge with the PDF rendering library, which is producing incorrect page breaks on invoices with more than 40 line items. We are currently investigating potential solutions, and we may need some additional time depending on how it goes. It would be really helpful if we could get a decision on whether we can ship CSV first and follow with PDF. Additionally, Mark will be out next week, which might affect the timeline slightly. Please let me know if you have any questions or would like to discuss further. Thanks so much!

**CRISP**
> Sarah, CSV export is on staging. PDF export is 60% done and blocked: the rendering library breaks pages wrongly on invoices with more than 40 line items, and we have no fix yet.
>
> Decision needed from you: can we ship CSV first and PDF after? PDF may slip. How much depends on the page-break fix. Mark is out next week.

Words: 175 → 60 (−66%). Removed: greeting, vague progress claims, padding, closing offer.

Kept: the unknown delay, with what resolves it (the page-break fix). A status update that hid it would be a surprise later.

### Research answer

*Prompt: "Does telling an LLM to be brief make it less accurate?"*

**Before**
> That's a really interesting and important question that has received quite a bit of attention from researchers recently! Let me provide a comprehensive overview of what the current research says.
>
> There have been several studies investigating this topic, and the results are somewhat mixed. On the one hand, some research suggests that asking models to be concise can be beneficial. For example, Renze and Guven (2024) found that a concise chain-of-thought prompt reduced response length by 48.7% with negligible changes in accuracy on multiple-choice question answering, while also lowering per-token cost by 22.7%.
>
> On the other hand, there is also evidence that brevity can be harmful in certain situations. The same study found that GPT-3.5 lost 27.69% accuracy on math problems with concise reasoning. Additionally, Giskard's Phare analysis (2025) found that instructing models to answer briefly lowered their resistance to hallucination by up to 20%, as refuting a false claim often requires more space.
>
> Overall, the research suggests that the impact of brevity instructions depends on a variety of factors, including the model and task type. It's important to note that more research is needed. In conclusion, while concision can be helpful, it should be used thoughtfully. I hope this overview is helpful!

**CRISP**
> Brevity instructions cost little on easy tasks (one small study) and hurt math and false-premise rebuttals.
>
> - Easy tasks: a concise chain-of-thought prompt cut response length 48.7% and per-token cost 22.7%, with negligible accuracy change on multiple-choice QA (Renze and Guven, 2024).
> - Math: the same concise prompt cost GPT-3.5 27.69% accuracy (same study).
> - False-premise questions: "answer briefly" lowered hallucination resistance by up to 20%, because a rebuttal needs space (Giskard Phare, 2025).

Words: 203 → 74 (−64%). Removed: praise opener, "mixed results" framing, generic conclusion, closer.

Kept: the two conditions where brevity hurts. Dropping them would turn a nuanced finding into "brevity is free".

### Specification

*Task: "Write requirements for a password reset by email."*

**Before**
> Here is a comprehensive specification for the password reset feature. Please find the requirements below.
>
> The system should provide users with a seamless and secure way to reset their passwords. Users should be able to request a password reset by entering their email address, and the system should send them an email containing a reset link as soon as possible. The link should be valid for a reasonable amount of time, ideally around 30 minutes, and should only be usable once. It's crucial that the system does not reveal whether an email address is registered, so the same message should be displayed in all cases. Appropriate rate limiting should be applied to prevent abuse, such as 5 requests per hour per IP address. The new password should meet our existing password policy requirements. After a successful reset, all existing sessions for the user should be invalidated, and the user should be notified by email.
>
> In summary, these requirements should ensure a robust and user-friendly password reset experience. Please let me know if any clarifications are needed.

**CRISP**
> Request:
> - The user enters their email address and the system sends a reset link.
> - The response is identical whether or not the address is registered.
> - Limit requests to 5 per hour per IP address.
>
> The link expires after 30 minutes and works once.
>
> The new password must meet the existing password policy. On success, invalidate all of the user's sessions and send a confirmation email.

Words: 176 → 68 (−61%). Removed: announcement, vague qualifiers, summary, closer.

### Agent-to-agent delegation

*Situation: a parent agent briefs a subagent.*

**Before**
> Hello! I hope you're doing well. I have an important task for you today. I would like you to please take a look at our repository and investigate the flaky tests, as they have been causing quite a few problems for the team recently. I think it would be really helpful if you could carefully analyze the test suite and try to identify which tests are flaky and why. You might want to start with the `tests/integration/` directory, since I believe that's where most of the problems are, though I haven't confirmed that. To find them, run each test several times, say 5, and treat any test with differing results as flaky. Please don't make any changes to the code, as I just want to understand the situation first. When you're done, it would be great if you could provide a detailed report with all your findings, including any recommendations you may have. Please take your time and be as thorough as possible, and let me know if anything is unclear. Thanks in advance for your help!

**CRISP**
> Find the flaky tests in `tests/integration/` and the likely cause of each. I expect most flakiness there but haven't confirmed it, so stop after that directory and report; I'll decide on the rest.
>
> - Run each test 5 times. A test is flaky if its results differ between runs.
> - Read-only: don't edit any code.
> - Reply with one line per flaky test: name, failures out of 5, likely cause (mark unconfirmed causes as unconfirmed), plus any recommendations.
>
> Done when every test in the directory has run 5 times.

Words: 177 → 89 (−50%). Removed: greeting, motivation, "be thorough" boilerplate, thanks.

Full protocol: https://github.com/andreiverdes/crisp/blob/main/CRISP.md
