import pandas as pd
import sys

try:
    print("Loading dataset...")
    df = pd.read_parquet("hf://datasets/argilla/pc-components-reviews/data/train-00000-of-00001.parquet")
    print("Dataset loaded successfully.")
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nSample Texts:")
    for t in df['text'].head(5):
        print(f"- {t[:200]}...") # Print first 200 chars

except Exception as e:
    print(f"Error: {e}")
