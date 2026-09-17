import streamlit as st
from src.agent import SupportAgent
st.set_page_config(page_title="TrustDesk",layout="centered")
st.title("TrustDesk — Apple Support Agent")
st.caption("Retrieval-grounded prototype with conservative escalation.")
agent=SupportAgent()
text=st.text_area("Customer message",placeholder="Type a customer support message...")
if st.button("Analyze") and text.strip():
    r=agent.predict(text.strip())
    st.subheader("Decision")
    st.write("**Intent:**",r["intent"])
    st.write("**Confidence:**",f"{r['confidence']:.3f}")
    st.write("**Auto-handle:**",r["auto_handle"])
    if r["escalate_reasons"]: st.write("**Escalation reasons:**",", ".join(r["escalate_reasons"]))
    st.subheader("Draft reply")
    st.write(r["reply"])
    st.subheader("Historical evidence")
    for e in r["evidence"]:
        with st.expander(f"Similarity {e['similarity']:.3f}"):
            st.write("Customer:",e["customer_text"])
            st.write("Historical response:",e["response_text"])
