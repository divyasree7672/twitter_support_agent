import os, json, joblib, numpy as np, pandas as pd
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
from src.agent import SupportAgent
os.makedirs("reports",exist_ok=True)
g=pd.read_csv("data/golden/golden.csv").fillna("")
g=g[g.expected_intent!=""].copy()
agent=SupportAgent()
pred=[]; conf=[]; auto=[]; sim=[]; replies=[]; reasons=[]
for t in g.customer_text:
    r=agent.predict(t)
    pred.append(r["intent"]); conf.append(r["confidence"]); auto.append(r["auto_handle"])
    sim.append(r["evidence"][0]["similarity"] if r["evidence"] else 0)
    replies.append(r["reply"]); reasons.append("|".join(r["escalate_reasons"]))
majority=g.expected_intent.value_counts().idxmax()
metrics={
"gold_n":len(g),
"proposed_accuracy":float(accuracy_score(g.expected_intent,pred)),
"proposed_macro_f1":float(f1_score(g.expected_intent,pred,average="macro")),
"majority_accuracy":float((g.expected_intent==majority).mean()),
"auto_handle_rate":float(np.mean(auto)),
"auto_intent_accuracy":float(accuracy_score(g.loc[np.array(auto), "expected_intent"],np.array(pred)[np.array(auto)])) if any(auto) else None,
"mean_top1_retrieval_similarity":float(np.mean(sim)),
"escalation_rate":float(1-np.mean(auto)),
}
json.dump(metrics,open("reports/metrics.json","w"),indent=2)
with open("reports/metrics.md","w") as f:
    f.write("# Evaluation\n\n")
    for k,v in metrics.items(): f.write(f"- **{k}:** {v}\n")
    f.write(f"\nMajority baseline label: `{majority}`\n\n")
    f.write("## Classification report\n\n```text\n")
    f.write(classification_report(g.expected_intent,pred,digits=3))
    f.write("```\n")
pd.DataFrame({"text":g.customer_text,"expected":g.expected_intent,"predicted":pred,"confidence":conf,"top1_similarity":sim,"auto_handle":auto,"reasons":reasons,"reply":replies}).to_csv("reports/failure_examples.csv",index=False)
print(json.dumps(metrics,indent=2))
