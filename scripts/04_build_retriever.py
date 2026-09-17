import os, joblib, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
PAIRS="data/processed/apple_pairs.csv"
df=pd.read_csv(PAIRS).fillna("")
vec=TfidfVectorizer(ngram_range=(1,2),min_df=2,max_features=100000,sublinear_tf=True)
X=vec.fit_transform(df.customer_text)
nn=NearestNeighbors(n_neighbors=10,metric="cosine",algorithm="brute").fit(X)
os.makedirs("models",exist_ok=True)
joblib.dump(vec,"models/retriever_vectorizer.joblib")
joblib.dump(nn,"models/retriever_nn.joblib")
df.to_pickle("models/retriever_pairs.pkl")
print(f"Retriever built on {len(df):,} historical customer-response pairs.")
