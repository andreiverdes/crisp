# Judge prompt (crisp-bench/v1)

Use verbatim. Fill `{{...}}`. Send as a single user message, no system prompt, reasoning `high`. Parse the JSON block in the reply.

---

You are judging two answers to the same prompt. You do not know which is which. Judge only what is on the page.

PROMPT GIVEN TO BOTH:
<prompt>
{{prompt}}
</prompt>

REQUIRED FACTS (an answer is complete only if it states each of these, in any wording):
{{required_facts_list}}   <!-- one line each: "f1: <fact>" -->

ANSWER A:
<answer_a>
{{answer_a}}
</answer_a>

ANSWER B:
<answer_b>
{{answer_b}}
</answer_b>

Score each answer 1-5 on each dimension. Use the whole scale.

- correctness: 5 = no technical errors; 1 = materially wrong.
- clarity: 5 = understood on first read; 1 = must be decoded.
- ambiguity: 5 = nothing vague, every reference and condition is clear; 1 = vague terms, unclear references, hidden assumptions.
- scanability: 5 = the key point and structure are findable in seconds, and formatting matches the content; 1 = the point is buried, or formatting is decorative or excessive.
- relevance: 5 = everything serves the question; 1 = padding, generic advice, unasked tangents, restated question or context.
- conversational: 5 = sounds like a competent colleague talking; 1 = robotic, bureaucratic, academic, or chatty filler ("Sure!", "Great question", "In conclusion").
- completeness: 5 = everything the asker needs to act, nothing essential missing; 1 = key parts missing.

Then, for each required fact, say whether each answer states it.

Then note useful content that one answer has and the other lacks, beyond the required facts: anything a competent reader would want and could act on. Ignore padding, generic advice, and restated context. If nothing useful is missing from either, use an empty string.

Then choose which answer a competent engineer would rather receive. Length is not a virtue or a flaw by itself; judge usefulness per word.

Reply with only a JSON object in this shape. All scores are integers 1-5. `preferred` is exactly one of "A", "B", "tie". Example values shown:

```json
{
  "A": {"correctness": 4, "clarity": 3, "ambiguity": 4, "scanability": 3, "relevance": 3, "conversational": 3, "completeness": 4,
        "facts_present": ["f1", "f2", "f4"]},
  "B": {"correctness": 4, "clarity": 5, "ambiguity": 4, "scanability": 5, "relevance": 5, "conversational": 4, "completeness": 4,
        "facts_present": ["f1", "f2", "f3", "f4"]},
  "useful_lost": {"A": "B explains the Retry-After calculation; A does not.", "B": ""},
  "preferred": "B",
  "notes": "one or two sentences: the decisive difference"
}
```
