import re
import pandas as pd

def clean_text(x):
    if pd.isna(x):
        return ""
    x = str(x)
    x = re.sub(r"\s+", " ", x).strip()
    return x

def parse_ids(x):
    if pd.isna(x) or str(x).strip() == "":
        return []
    return [v.strip() for v in str(x).split(",") if v.strip()]
