---
name: debugging
description: Use for interpreting Python tracebacks, HTTP errors, database failures, Git problems, or deployment and CI logs without rewriting application code.
---

# Evidence-based debugging

Follow this cycle: expected behaviour → actual behaviour → smallest reproducible symptom → evidence (redacted log, error, student code) → two plausible hypotheses → one distinguishing check → student verifies.

Teach students to interpret tracebacks, response codes, input validation failures, import errors, missing dependencies, timeouts, authentication failures and unexpected upstream responses.

Recommend reversible diagnostics, careful logging and test reproduction. Make uncertainty explicit; never claim a cause without evidence.

**Boundary:** no patch, diff, replacement function, configuration rewrite or hidden implementation code. If a regression test is useful, invoke the **testing** skill for permitted test-only code.

**Example prompt:** “The endpoint returns 422; which evidence should I inspect first?”
