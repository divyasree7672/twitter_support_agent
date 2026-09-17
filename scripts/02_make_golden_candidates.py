import argparse, os, pandas as pd
from sklearn.model_selection import train_test_split

INTENTS = [
"account_login_access","billing_payment","purchase_refund","device_hardware",
"app_software_issue","subscription_service","delivery_order","general_support"
]
ap=argparse.ArgumentParser()
ap.add_argument("--input",default="data/processed/apple_pairs.csv")
ap.add_argument("--output",default="data/golden/golden.csv")
ap.add_argument("--n",type=int,default=220)
a=ap.parse_args()
df=pd.read_csv(a.input)
# Stratify by coarse text-length buckets to avoid a golden set made only of long tweets.
df["bucket"]=pd.qcut(df["customer_text"].str.len().rank(method="first"), q=5, labels=False, duplicates="drop")
n=min(a.n,len(df))
sample=df.groupby("bucket", group_keys=False).apply(lambda x:x.sample(max(1,round(n*len(x)/len(df))), random_state=42)).head(n)
out=pd.DataFrame({
"example_id":range(1,len(sample)+1),
"customer_text":sample["customer_text"].values,
"expected_intent":[""]*len(sample),
"notes":[""]*len(sample),
})
os.makedirs(os.path.dirname(a.output),exist_ok=True)
out.to_csv(a.output,index=False)
print(f"Created {len(out)} candidates at {a.output}. Open the Streamlit labeler and label every row.")
