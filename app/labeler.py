import sys
from pathlib import Path

# ---------------------------------------------------------
# Project root
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

import pandas as pd
import streamlit as st

from src.config import INTENTS


# ---------------------------------------------------------
# Golden file
# ---------------------------------------------------------

GOLDEN_PATH = PROJECT_ROOT / "data" / "golden" / "golden.csv"


# ---------------------------------------------------------
# Page settings
# ---------------------------------------------------------

st.set_page_config(
    page_title="Golden Set Labeler",
    layout="wide"
)

st.title("Golden Set Labeler")

st.write(
    "Read the customer message and select the most appropriate intent."
)


# ---------------------------------------------------------
# Check file
# ---------------------------------------------------------

if not GOLDEN_PATH.exists():
    st.error(f"Golden file not found: {GOLDEN_PATH}")
    st.stop()


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

df = pd.read_csv(GOLDEN_PATH)


# ---------------------------------------------------------
# Make sure columns exist
# ---------------------------------------------------------

if "expected_intent" not in df.columns:
    df["expected_intent"] = ""

if "notes" not in df.columns:
    df["notes"] = ""


# Convert to text so Pandas can store intent names
df["expected_intent"] = (
    df["expected_intent"]
    .fillna("")
    .astype(str)
)

df["notes"] = (
    df["notes"]
    .fillna("")
    .astype(str)
)


# ---------------------------------------------------------
# Find first unlabelled example
# ---------------------------------------------------------

unlabelled = (
    df["expected_intent"]
    .str.strip()
    .eq("")
)


if unlabelled.any():
    idx = unlabelled.idxmax()
else:
    idx = len(df)


# ---------------------------------------------------------
# Count labelled examples
# ---------------------------------------------------------

labelled_count = (
    df["expected_intent"]
    .str.strip()
    .ne("")
    .sum()
)


# ---------------------------------------------------------
# Finished
# ---------------------------------------------------------

if labelled_count >= len(df):

    st.success(" All 200 examples have been labelled!")

    st.write(
        f"Completed: **{labelled_count} / {len(df)}**"
    )

    st.stop()


# ---------------------------------------------------------
# Progress
# ---------------------------------------------------------

st.progress(
    labelled_count / len(df)
)

st.write(
    f"Example **{idx + 1} / {len(df)}**"
)

st.write(
    f"Already labelled: **{labelled_count} / {len(df)}**"
)


# ---------------------------------------------------------
# Current customer
# ---------------------------------------------------------

row = df.iloc[idx]


st.subheader("Customer message")

st.info(
    str(row["customer_text"])
)


# ---------------------------------------------------------
# Historical response
# ---------------------------------------------------------

if "response_text" in df.columns:

    response = str(row["response_text"])

    if response != "nan":

        st.subheader("Historical brand response")

        st.write(response)


# ---------------------------------------------------------
# Intent descriptions
# ---------------------------------------------------------

intent_help = {

    "account_login_access":
        "Login, password, account access or locked account problem.",

    "billing_payment":
        "Payment failed, charged, card/payment problem or duplicate charge.",

    "purchase_refund":
        "Customer wants a refund, return or reimbursement.",

    "device_hardware":
        "Physical Apple device problem: iPhone, iPad, Mac, Watch, battery, screen, charging etc.",

    "app_software_issue":
        "App, iOS, macOS, update, crash, settings or software problem.",

    "subscription_service":
        "Apple Music, iCloud or another subscription, plan, cancellation or renewal problem.",

    "delivery_order":
        "Order, shipping, delivery, tracking or missing package problem.",

    "general_support":
        "General question or issue that does not clearly fit another category."
}


# ---------------------------------------------------------
# Intent selection
# ---------------------------------------------------------

selected_intent = st.selectbox(
    "Select Intent",
    INTENTS,
    format_func=lambda x:
        f"{x} — {intent_help.get(x, '')}"
)


# ---------------------------------------------------------
# Notes
# ---------------------------------------------------------

notes = st.text_area(
    "Notes (optional)",
    value=""
)


# ---------------------------------------------------------
# Save & Next
# ---------------------------------------------------------

if st.button(
    "Save & Next",
    type="primary"
):

    df.loc[idx, "expected_intent"] = selected_intent
    df.loc[idx, "notes"] = notes

    df.to_csv(
        GOLDEN_PATH,
        index=False
    )

    st.rerun()


# ---------------------------------------------------------
# Quick guide
# ---------------------------------------------------------

st.divider()

st.subheader("Quick Intent Guide")

for intent in INTENTS:

    st.write(
        f"**{intent}** → "
        f"{intent_help.get(intent, '')}"
    )