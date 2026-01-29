import pandas as pd
import os
import sys

print("=" * 50)
print("TESTING DATA LOADING")
print("=" * 50)

# Check current directory
print(f"Current directory: {os.getcwd()}")

# Try to find the file
file_path = "../data/raw/election_tweets_sample.csv"
print(f"\nLooking for: {file_path}")
print(f"File exists: {os.path.exists(file_path)}")

if os.path.exists(file_path):
    print("\n✅ File found! Trying to load...")
    
    # Try to read just first 1000 rows to test
    try:
        df = pd.read_csv(file_path, nrows=1000)
        print(f"✅ Successfully loaded {len(df)} rows")
        
        print(f"\nColumns found: {list(df.columns)}")
        print(f"\nFirst 2 rows:")
        for i in range(2):
            print(f"\nRow {i}:")
            for col in df.columns[:5]:  # Show first 5 columns
                print(f"  {col}: {df[col].iloc[i]}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}")
        print(f"Details: {e}")
        import traceback
        traceback.print_exc()
else:
    print("\n❌ File not found at that path")
    
    # List what's in data/raw
    raw_dir = "../data/raw"
    if os.path.exists(raw_dir):
        print(f"\nFiles in {raw_dir}:")
        for f in os.listdir(raw_dir):
            print(f"  - {f}")