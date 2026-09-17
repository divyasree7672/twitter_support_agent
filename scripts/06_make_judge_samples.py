import json, pandas as pd
from src.agent import SupportAgent
g=pd.read_csv("data/golden/golden.csv").fillna("")
g=g[g.expected_intent!=""].sample(min(30,len(g)),random_state=7)
agent=SupportAgent()
with open("reports/judge_samples.jsonl","w") as f:
    for _,r in g.iterrows():
        p=agent.predict(r.customer_text)
        obj={"customer_message":r.customer_text,"expected_intent":r.expected_intent,
             "predicted_intent":p["intent"],"draft_reply":p["reply"],
             "evidence":p["evidence"][:3]}
        f.write(json.dumps(obj)+"\n")
print("Wrote reports/judge_samples.jsonl")
