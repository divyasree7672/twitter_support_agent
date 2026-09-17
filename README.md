# TrustDesk — Brand Customer-Support AI Agent

A reproducible project for the **Customer Support on Twitter** dataset. The default brand is **AppleSupport**.

## What the system does

1. **Intent classification**: classifies an inbound customer tweet into a small, data-derived intent taxonomy.
2. **Grounded reply drafting**: retrieves historically similar AppleSupport resolutions and drafts a response from those examples.
3. **Escalation**: sends low-confidence, sensitive, angry, or unsupported cases to a human and explains why.
4. **Evaluation**: evaluates intent accuracy, retrieval quality, escalation safety, and reply quality.

The architecture intentionally avoids pretending that a fluent LLM answer is evidence of correctness. The primary reply mechanism is retrieval from historical resolutions; an LLM is optional for rewriting a retrieved resolution.

## Dataset

Primary dataset: Thought Vector's Customer Support on Twitter, ~3M tweets. The Kaggle data has columns `tweet_id`, `author_id`, `inbound`, `created_at`, `text`, `response_tweet_id`, and `in_response_to_tweet_id`. See:
https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter

The dataset is noisy and the full dataset is large, so the pipeline samples/filters only the selected brand.

### Download

Download `twcs.csv` from Kaggle and place it at:

`data/raw/twcs.csv`

Do not commit the raw dataset.

## 15-minute reproduction

Create an environment:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Prepare data:

```bash
python scripts/01_prepare.py --input data/raw/twcs.csv --brand AppleSupport --max-pairs 60000
```

Create a candidate set for manual golden labeling:

```bash
python scripts/02_make_golden_candidates.py --n 220
```

Open the labeling UI:

```bash
streamlit run app/labeler.py
```

After labeling 150–250 examples:

```bash
python scripts/03_train.py
python scripts/04_build_retriever.py
python scripts/05_evaluate.py
```

Run the agent:

```bash
streamlit run app/agent_ui.py
```

## Important: the golden set is genuinely human-labelled

The repository includes the *candidate sampler* and labeling interface, but it must not fabricate a human gold standard. Label 150–250 examples yourself. This is a required part of the challenge and is the strongest protection against misleading evaluation.

Recommended split:
- 150 examples: minimum viable gold set
- 200 examples: preferred
- 250 examples: strongest

Use the same intent definitions for all labels.

## Intent taxonomy

Start with 8 intents. These are deliberately broad enough to get useful support coverage while remaining labelable:

- `account_login_access`
- `billing_payment`
- `purchase_refund`
- `device_hardware`
- `app_software_issue`
- `subscription_service`
- `delivery_order`
- `general_support`

The preparation script creates a labeling file with these choices. If your sample shows that one category is rare or ambiguous, change the taxonomy and document the decision in `reports/decision_log.md`.

## Reply strategy

For each new message:

1. Predict intent and confidence.
2. Retrieve top historical customer→company response pairs.
3. Require a minimum similarity score.
4. If safe, draft from the retrieved resolution pattern.
5. If evidence is weak or the case is sensitive, escalate.
6. Never invent account-specific actions.

The default draft is extractive/retrieval-grounded. This makes the source of the answer inspectable.

## Baselines

The evaluation compares:

### Baseline A — majority intent
Always predicts the most common intent in the training set.

### Baseline B — lexical nearest neighbour
Uses TF-IDF cosine similarity and copies the response associated with the closest training customer message.

### Proposed system
TF-IDF logistic-regression intent classifier + top-k historical retrieval + explicit escalation policy.

## Headline metrics

`05_evaluate.py` writes:

- `reports/metrics.json`
- `reports/metrics.md`
- `reports/confusion_matrix.png`
- `reports/failure_examples.csv`

Do not headline one metric only. Report:
- intent macro-F1
- intent accuracy
- retrieval Recall@5
- safe-auto-handling precision
- escalation rate
- reply evidence coverage
- human/LLM judge agreement if a judge is used

## LLM-as-judge

The harness supports a judge input/output contract rather than hard-coding one vendor.

`python scripts/06_llm_judge.py --input reports/judge_samples.jsonl --output reports/judge_scores.jsonl`

The judge receives:
- customer message
- predicted intent
- drafted reply
- retrieved historical evidence

It scores:
- relevance: 0–2
- groundedness: 0–2
- actionability: 0–2
- tone: 0–2
- unsupported claims: 0–2 (reverse-scored)

A separate human subset should be scored with the same rubric. Report exact agreement and weighted Cohen's kappa.

## Mandatory “What is misleading about my headline number?”

Put this in the report:

> A high intent F1 does not prove the agent is safe to deploy. The golden set is small and hand-labelled; historical Twitter conversations are not a representative sample of today's support traffic; retrieval similarity is not the same as factual correctness; and an LLM judge can share the system's blind spots. Auto-handling therefore uses a conservative escalation policy rather than treating the headline metric as a deployment guarantee.

## Failure analysis

The evaluation script surfaces examples for:
1. ambiguous multi-intent messages
2. short/underspecified tweets
3. unseen issues
4. retrieval mismatch
5. sensitive/account-specific requests

For each, document:
- message
- expected intent
- prediction
- evidence retrieved
- failure mechanism
- proposed fix

## One-more-week plan

1. Expand the gold set to 500–1,000 examples.
2. Add time-based evaluation to test drift.
3. Compare dense embeddings against TF-IDF.
4. Add a human escalation review queue.
5. Build adversarial tests for hallucinated refunds, account actions, and policy claims.
6. Add confidence calibration.
7. Add privacy/PII checks.
8. Evaluate multiple brands to test whether the architecture generalizes.

## Decision log

See `reports/decision_log.md`.
