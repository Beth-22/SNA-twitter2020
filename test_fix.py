import sys
import os

print("TEST 1: Basic print")
print(f"Python version: {sys.version}")
print(f"Current dir: {os.getcwd()}")

# Force flush
sys.stdout.flush()

# Check file
file_path = "data/raw/election_tweets_sample.csv"
print(f"\nLooking for: {file_path}")
print(f"File exists: {os.path.exists(file_path)}")

sys.stdout.flush()

# Try to read file
if os.path.exists(file_path):
    print("\nTrying to read file...")
    sys.stdout.flush()
    
    # Try with import
    try:
        import pandas as pd
        print("Pandas imported successfully")
        
        # Read just first 10 rows
        df = pd.read_csv(file_path, nrows=10)
        print(f"Read {len(df)} rows")
        print(f"Columns: {list(df.columns)}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    sys.stdout.flush()

print("\nTest complete!")
sys.stdout.flush()