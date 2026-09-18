# TrustDesk — Brand Customer-Support AI Agent

A reproducible AI customer-support agent built using the Customer Support on Twitter dataset.

The default brand used in this project is **AppleSupport**.

## What the system does

The system performs three main tasks:

1. **Intent classification**  
   Classifies an incoming customer message into a small set of support intents.

2. **Grounded reply drafting**  
   Retrieves historically similar AppleSupport conversations and uses those examples to draft a response.

3. **Human escalation**  
   Decides whether the message can be handled automatically or should be escalated to a human, with a stated reason.

The system is designed to prefer historical evidence over unsupported generated answers.

---

## Dataset

Primary dataset:

**Customer Support on Twitter (TWCS)** by Thought Vector.

The dataset contains approximately 3 million tweets from multiple customer-support brands.

The dataset includes fields such as:

- `tweet_id`
- `author_id`
- `inbound`
- `created_at`
- `text`
- `response_tweet_id`
- `in_response_to_tweet_id`

The raw dataset is not included in this repository because of its size.

Download the dataset and place it at:

```text
data/raw/twcs.csv