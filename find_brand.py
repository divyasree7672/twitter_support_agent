import pandas as pd

file_path = "data/raw/twcs.csv"

df = pd.read_csv(
    file_path,
    usecols=["author_id", "inbound", "text"]
)

print("Total tweets:", len(df))

print("\nOutbound author IDs:")
print(
    df[df["inbound"] == False]["author_id"]
    .value_counts()
    .head(30)
)