import argparse, os
import pandas as pd
from .utils import clean_text

def prepare(input_path, output_path, brand="AppleSupport", max_pairs=60000):
    df = pd.read_csv(input_path)
    required = {"tweet_id","author_id","inbound","created_at","text","response_tweet_id","in_response_to_tweet_id"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    # Company author IDs can be inferred from outbound tweets.
    outbound = df[df["inbound"] == False]
    company_ids = set(outbound["author_id"].dropna().astype(str))
    # The dataset has anonymized author IDs; brand handles are recoverable from
    # the inbound/outbound structure. For AppleSupport, use the author's outbound
    # activity and select the largest support identity.
    counts = outbound["author_id"].astype(str).value_counts()
    if counts.empty:
        raise ValueError("No outbound tweets found.")

    # In the standard TWCS file, the largest outbound support identity is
    # generally a major brand. If a direct handle mapping is present in text
    # or an AppleSupport-filtered file is supplied, use it. Otherwise use the
    # brand_id stored in config/brand_map.csv when available.
    map_path = "data/raw/brand_map.csv"
    if os.path.exists(map_path):
        bm = pd.read_csv(map_path)
        row = bm[bm["brand"].str.lower() == brand.lower()]
        if len(row):
            company_id = str(row.iloc[0]["company_author_id"])
        else:
            company_id = str(counts.index[0])
    else:
        # Fallback for the standard dataset: require an explicit company id.
        # This avoids silently assigning a wrong brand.
        raise ValueError(
            "Create data/raw/brand_map.csv with columns brand,company_author_id. "
            "Use the outbound author_id for the chosen brand. "
            "This prevents accidentally evaluating the wrong company."
        )

    brand_df = df[df["author_id"].astype(str).eq(company_id) | df["in_response_to_tweet_id"].notna()].copy()
    # Keep only customer->company pairs whose response is an outbound tweet.
    by_id = df.set_index(df["tweet_id"].astype(str))
    rows = []
    for _, r in df[df["inbound"] == True].iterrows():
        response_ids = str(r.get("response_tweet_id",""))
        if response_ids == "nan" or not response_ids:
            continue
        rid = response_ids.split(",")[0].strip()
        if rid not in by_id.index:
            continue
        resp = by_id.loc[rid]
        if str(resp["author_id"]) != company_id:
            continue
        rows.append({
            "customer_tweet_id": str(r["tweet_id"]),
            "customer_text": clean_text(r["text"]),
            "response_tweet_id": str(resp["tweet_id"]),
            "response_text": clean_text(resp["text"]),
            "created_at": r["created_at"],
        })
        if len(rows) >= max_pairs:
            break

    out = pd.DataFrame(rows).drop_duplicates("customer_tweet_id")
    if len(out) < 500:
        raise ValueError(f"Only {len(out)} pairs found. Check brand_map.csv/company_author_id.")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    out.to_csv(output_path, index=False)
    print(f"Wrote {len(out):,} customer-response pairs to {output_path}")

if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", default="data/processed/apple_pairs.csv")
    ap.add_argument("--brand", default="AppleSupport")
    ap.add_argument("--max-pairs", type=int, default=60000)
    a=ap.parse_args()
    prepare(a.input,a.output,a.brand,a.max_pairs)
