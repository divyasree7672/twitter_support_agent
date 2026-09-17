"""
Vendor-neutral LLM judge.

Input: reports/judge_samples.jsonl
Output: reports/judge_scores.jsonl

Set JUDGE_API_URL and JUDGE_API_KEY for an OpenAI-compatible chat-completions
endpoint. The script intentionally sends only the sampled message/reply/evidence.

The model must return JSON:
{
 "relevance": 0-2,
 "groundedness": 0-2,
 "actionability": 0-2,
 "tone": 0-2,
 "unsupported_claims": 0-2,
 "reason": "short explanation"
}
"""
import os,json,requests,argparse
PROMPT="""You are evaluating a customer-support AI reply.
Score independently:
relevance (0-2), groundedness (0-2), actionability (0-2), tone (0-2),
unsupported_claims (0-2 where 2 means many unsupported claims).
Use the historical evidence as the grounding source. Do not reward fluency alone.
Return JSON only."""
ap=argparse.ArgumentParser(); ap.add_argument("--input",required=True); ap.add_argument("--output",required=True); a=ap.parse_args()
url=os.getenv("JUDGE_API_URL"); key=os.getenv("JUDGE_API_KEY"); model=os.getenv("JUDGE_MODEL","judge")
if not url or not key: raise SystemExit("Set JUDGE_API_URL, JUDGE_API_KEY and optionally JUDGE_MODEL.")
headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"}
with open(a.input) as fi,open(a.output,"w") as fo:
    for line in fi:
        item=json.loads(line)
        body={"model":model,"temperature":0,"messages":[
            {"role":"system","content":PROMPT},
            {"role":"user","content":json.dumps(item)}
        ]}
        r=requests.post(url,headers=headers,json=body,timeout=90); r.raise_for_status()
        content=r.json()["choices"][0]["message"]["content"]
        try: score=json.loads(content)
        except Exception: score={"parse_error":True,"raw":content}
        fo.write(json.dumps({**item,"judge":score})+"\n")
print("Judge results written.")
