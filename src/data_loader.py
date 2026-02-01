import pandas as pd
import os
import sys

def load_twitter_data(file_path=None):
    """
    Load Twitter election dataset
    """
    print("Starting data loader...")
    
    if file_path is None:
        # Default path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        file_path = os.path.join(project_root, 'data', 'raw', 'election_tweets_sample.csv')
    
    print(f"Looking for file at: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    if not os.path.exists(file_path):
        print("ERROR: File does not exist!")
        print("Current working directory:", os.getcwd())
        print("Please check the file path.")
        return None
    
    try:
        print(f"\nAttempting to load CSV file...")
        # Try different encodings if needed
        try:
            df = pd.read_csv(file_path)
        except UnicodeDecodeError:
            print("Trying latin1 encoding...")
            df = pd.read_csv(file_path, encoding='latin1')
        
        print(f"✅ Successfully loaded {len(df)} tweets")
        
        # Show basic info
        print("\n=== DATASET INFO ===")
        print(f"Columns: {list(df.columns)}")
        print(f"Shape: {df.shape} (rows x columns)")
        
        # Show first few rows
        print("\n=== FIRST 3 ROWS ===")
        print(df.head(3))
        
        return df
    
    except Exception as e:
        print(f"❌ Error loading data: {type(e).__name__}")
        print(f"Error details: {e}")
        return None

def explore_data(df):
    """
    Explore the dataset structure
    """
    if df is None:
        print("No data to explore!")
        return
    
    print("\n=== DATA EXPLORATION ===")
    
    # Check for missing values
    print("\nMissing values per column:")
    missing = df.isnull().sum()
    for col, count in missing.items():
        if count > 0:
            print(f"  {col}: {count} missing")
    
    # Check data types
    print("\nData types (first 10 columns):")
    for col, dtype in df.dtypes.items()[:10]:
        print(f"  {col}: {dtype}")
    
    # Check unique users
    user_cols = ['user_name', 'user_screen_name', 'username', 'user']
    for col in user_cols:
        if col in df.columns:
            print(f"\nUnique users in '{col}': {df[col].nunique()}")
            break
    
    # Show sample of user mentions/retweets
    print("\n=== SAMPLE TEXTS (first 2) ===")
    text_cols = ['text', 'tweet', 'content']
    for col in text_cols:
        if col in df.columns:
            for i in range(min(2, len(df))):
                print(f"\nTweet {i+1}: {df[col].iloc[i][:100]}...")
            break

if __name__ == "__main__":
    print("=" * 50)
    print("TWITTER DATA LOADER - 2020 ELECTION ANALYSIS")
    print("=" * 50)
    
    df = load_twitter_data()
    if df is not None:
        explore_data(df)
    
    print("\n" + "=" * 50)
    print("Data loading complete!")
    print("=" * 50)