# Evaluation

- **gold_n:** 200
- **proposed_accuracy:** 0.865
- **proposed_macro_f1:** 0.8447360385197777
- **majority_accuracy:** 0.49
- **auto_handle_rate:** 0.02
- **auto_intent_accuracy:** 1.0
- **mean_top1_retrieval_similarity:** 1.0
- **escalation_rate:** 0.98

Majority baseline label: `app_software_issue`

## Classification report

```text
                      precision    recall  f1-score   support

account_login_access      1.000     0.714     0.833         7
  app_software_issue      0.871     0.898     0.884        98
     billing_payment      1.000     0.833     0.909         6
     device_hardware      0.918     0.865     0.891        52
     general_support      0.735     0.833     0.781        30
subscription_service      0.833     0.714     0.769         7

            accuracy                          0.865       200
           macro avg      0.893     0.810     0.845       200
        weighted avg      0.870     0.865     0.866       200
```
