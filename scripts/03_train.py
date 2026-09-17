import os, json, pandas as pd, joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
GOLD="data/golden/golden.csv"; PAIRS="data/processed/apple_pairs.csv"
os.makedirs("models",exist_ok=True)
g=pd.read_csv(GOLD).fillna("")
g=g[g.expected_intent!=""].copy()
if len(g)<150: raise SystemExit("Need at least 150 labelled examples.")
# Use only gold labels for supervised intent learning.
X_train,X_test,y_train,y_test=train_test_split(g.customer_text,g.expected_intent,test_size=.25,random_state=42,stratify=g.expected_intent)
model=Pipeline([
("tfidf",TfidfVectorizer(ngram_range=(1,2),min_df=2,max_df=.98,sublinear_tf=True)),
("clf",LogisticRegression(max_iter=2000,class_weight="balanced"))
])
model.fit(X_train,y_train)
joblib.dump(model,"models/intent_model.joblib")
pred=model.predict(X_test)
print(classification_report(y_test,pred,digits=3))
pd.DataFrame({"text":X_test,"y_true":y_test,"y_pred":pred}).to_csv("reports/intent_holdout.csv",index=False)
# majority baseline label learned from the same gold set
majority=g.expected_intent.value_counts().idxmax()
json.dump({"majority_intent":majority,"n_gold":len(g)},open("models/meta.json","w"),indent=2)
print("Saved models/intent_model.joblib")
