INTENTS = [
    "account_login_access",
    "billing_payment",
    "purchase_refund",
    "device_hardware",
    "app_software_issue",
    "subscription_service",
    "delivery_order",
    "general_support",
]

ESCALATION_REASONS = {
    "low_intent_confidence": "Intent confidence is below the auto-handling threshold.",
    "low_retrieval_similarity": "No sufficiently similar historical resolution was found.",
    "sensitive": "Message appears to request sensitive/account-specific handling.",
    "high_risk_language": "Message contains language indicating a potentially high-risk or highly dissatisfied case.",
}
