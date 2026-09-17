import re, joblib, pandas as pd, numpy as np

SENSITIVE_PATTERNS=[
r"\bpassword\b",r"\bpasscode\b",r"\bverification code\b",r"\bcredit card\b",
r"\bcard number\b",r"\baccount number\b",r"\bssn\b",r"\bsocial security\b"
]
HIGH_RISK=[r"\bsue\b",r"\blawsuit\b",r"\blawyer\b",r"\bchargeback\b",r"\bfraud\b",
           r"\bpolice\b",r"\bthreat\b"]

class SupportAgent:
    def __init__(self):
        self.intent=joblib.load("models/intent_model.joblib")
        self.vec=joblib.load("models/retriever_vectorizer.joblib")
        self.nn=joblib.load("models/retriever_nn.joblib")
        self.pairs=pd.read_pickle("models/retriever_pairs.pkl")

    def _flags(self,text):
        low=text.lower()
        return (
            any(re.search(p,low) for p in SENSITIVE_PATTERNS),
            any(re.search(p,low) for p in HIGH_RISK)
        )

    def retrieve(self,text,k=5):
        x=self.vec.transform([text])
        dist,idx=self.nn.kneighbors(x,n_neighbors=k)
        out=[]
        for d,i in zip(dist[0],idx[0]):
            r=self.pairs.iloc[i]
            out.append({"similarity":float(1-d),"customer_text":r.customer_text,"response_text":r.response_text})
        return out

    def predict(self,text):
        probs=self.intent.predict_proba([text])[0]
        classes=self.intent.classes_
        order=np.argsort(probs)[::-1]
        intent=classes[order[0]]
        confidence=float(probs[order[0]])
        evidence=self.retrieve(text,5)
        best=evidence[0]["similarity"] if evidence else 0
        sensitive,risk=self._flags(text)
        reasons=[]
        if confidence < .60: reasons.append("low_intent_confidence")
        if best < .30: reasons.append("low_retrieval_similarity")
        if sensitive: reasons.append("sensitive")
        if risk: reasons.append("high_risk_language")
        auto=(len(reasons)==0)
        reply=self._draft(text,intent,evidence) if auto else self._escalation(intent,reasons)
        return {"intent":intent,"confidence":confidence,"auto_handle":auto,
                "escalate_reasons":reasons,"reply":reply,"evidence":evidence}

    def _draft(self,text,intent,evidence):
        # Conservative template: use the historically observed resolution without inventing actions.
        if not evidence: return "Thanks for reaching out. We need a little more information to help."
        e=evidence[0]
        return f"Thanks for reaching out. Based on similar support cases, the relevant next step was: {e['response_text']}"

    def _escalation(self,intent,reasons):
        labels={
          "low_intent_confidence":"I’m not confident I understood the issue.",
          "low_retrieval_similarity":"I could not find a sufficiently similar historical resolution.",
          "sensitive":"This appears to involve sensitive or account-specific information.",
          "high_risk_language":"This case may need careful human review."
        }
        why=" ".join(labels[r] for r in reasons)
        return f"Thanks for reaching out. {why} I’m routing this to a support specialist rather than guessing."
