"""
Vendor-neutral LLM judge.

Input: reports/judge_samples.jsonl
Output: reports/llm_judge_results.jsonl

Requires:
  JUDGE_API_URL
  JUDGE_API_KEY
  JUDGE_MODEL
"""

import os
import json
import requests
import argparse
import time


PROMPT = """You are evaluating a customer-support AI reply.

Score independently:
relevance (0-2)
groundedness (0-2)
actionability (0-2)
tone (0-2)
unsupported_claims (0-2, where 2 means many unsupported claims)

Use the historical evidence as the grounding source.
Do not reward fluency alone.

Return JSON only:
{
  "relevance": 0,
  "groundedness": 0,
  "actionability": 0,
  "tone": 0,
  "unsupported_claims": 0,
  "reason": "short explanation"
}
"""


ap = argparse.ArgumentParser()
ap.add_argument("--input", required=True)
ap.add_argument("--output", required=True)
a = ap.parse_args()

url = os.getenv("JUDGE_API_URL")
key = os.getenv("JUDGE_API_KEY")
model = os.getenv("JUDGE_MODEL", "gpt-4o-mini")

if not url or not key:
    raise SystemExit(
        "Set JUDGE_API_URL, JUDGE_API_KEY and optionally JUDGE_MODEL."
    )

headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
}


with open(a.input, encoding="utf-8") as fi, open(
    a.output, "w", encoding="utf-8"
) as fo:

    for i, line in enumerate(fi, start=1):
        item = json.loads(line)

        body = {
            "model": model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": json.dumps(item)},
            ],
        }

        max_retries = 5

        for attempt in range(max_retries):
            try:
                r = requests.post(
                    url,
                    headers=headers,
                    json=body,
                    timeout=90,
                )

                if r.status_code == 429:
                    wait = 10 * (attempt + 1)
                    print(
                        f"Rate limited on sample {i}. "
                        f"Waiting {wait}s..."
                    )
                    time.sleep(wait)
                    continue

                r.raise_for_status()
                break

            except requests.RequestException as e:
                if attempt == max_retries - 1:
                    raise
                wait = 5 * (attempt + 1)
                print(
                    f"Request failed on sample {i}: {e}. "
                    f"Retrying in {wait}s..."
                )
                time.sleep(wait)

        else:
            raise SystemExit(
                f"Could not process sample {i} after {max_retries} retries."
            )

        content = r.json()["choices"][0]["message"]["content"]

        try:
            score = json.loads(content)
        except Exception:
            score = {
                "parse_error": True,
                "raw": content,
            }

        fo.write(
            json.dumps(
                {
                    **item,
                    "judge": score,
                },
                ensure_ascii=False,
            )
            + "\n"
        )

        fo.flush()

        print(f"Judged sample {i}")


print("Judge results written.")