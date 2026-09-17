# TrustDesk Evaluation Report

## 1. Problem framing

**Brand:** AppleSupport

**Good means:** correct intent, historically grounded resolution, clear and respectful reply, and conservative escalation when evidence is weak or the case is sensitive.

**Not built:** account access, payments/refunds execution, private-data collection, real-time policy lookup, or autonomous actions.

## 2. Data and sampling

Describe:
- number of AppleSupport customer→agent pairs
- date range
- cleaning
- train/gold split
- golden set sampling
- exact labelling instructions

## 3. Results

Paste `reports/metrics.json`.

Compare:
- Majority intent baseline
- lexical nearest-neighbour baseline
- proposed classifier + retrieval + escalation

Do not compare only accuracy. Include macro-F1 and auto-handling safety metrics.

## 4. Reply-quality evaluation

Report the LLM judge rubric and human agreement:
- exact agreement
- weighted Cohen's kappa
- mean scores
- examples of judge/human disagreement

## 5. Top five failure modes

For each:
1. Example
2. Expected
3. Predicted
4. Retrieved evidence
5. Why it failed
6. Hypothesis/fix

## 6. What is misleading about my headline number?

A high intent F1 does not prove the agent is safe to deploy. The gold set is small and hand-labelled; historical Twitter conversations are not a representative sample of today's support traffic; retrieval similarity is not factual verification; and an LLM judge can share the system's blind spots. Auto-handling is therefore evaluated separately from classification.

## 7. One more week

Expand gold data, add time-based drift tests, compare dense retrieval, add adversarial safety tests, calibrate confidence, add PII detection, and run a second-brand transfer experiment.
