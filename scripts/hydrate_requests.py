import requests
import json
import time
import sys
import os

def get_tweet_data(tweet_id):
    """Get tweet data using Twitter's syndication API"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://twitter.com/",
            "DNT": "1",
        }
        
        # Try the syndication API
        url = "https://cdn.syndication.twimg.com/tweet-result"
        params = {
            "id": tweet_id,
            "lang": "en",
            "features": "tfw_tweet_edit_backend:on"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Format the data
            formatted = {
                "id": tweet_id,
                "text": data.get("text", ""),
                "created_at": data.get("created_at", ""),
                "user": {
                    "id": data.get("user", {}).get("id_str", ""),
                    "name": data.get("user", {}).get("name", ""),
                    "screen_name": data.get("user", {}).get("screen_name", ""),
                    "profile_image_url": data.get("user", {}).get("profile_image_url_https", ""),
                    "verified": data.get("user", {}).get("verified", False),
                    "followers_count": data.get("user", {}).get("followers_count", 0),
                    "friends_count": data.get("user", {}).get("friends_count", 0),
                },
                "stats": {
                    "retweet_count": data.get("retweet_count", 0),
                    "favorite_count": data.get("favorite_count", 0),
                    "reply_count": data.get("reply_count", 0),
                    "quote_count": data.get("quote_count", 0),
                },
                "entities": {
                    "hashtags": data.get("entities", {}).get("hashtags", []),
                    "urls": data.get("entities", {}).get("urls", []),
                    "user_mentions": data.get("entities", {}).get("user_mentions", []),
                },
                "possibly_sensitive": data.get("possibly_sensitive", False),
                "lang": data.get("lang", ""),
                "source": data.get("source", ""),
            }
            
            # Add media if present
            if "photos" in data:
                formatted["media"] = [{"type": "photo", "url": photo["url"]} for photo in data["photos"]]
            elif "video" in data:
                formatted["media"] = [{"type": "video", "thumbnail_url": data["video"].get("poster", "")}]
            
            return formatted
        else:
            print(f"  HTTP {response.status_code} for tweet {tweet_id}")
            return None
            
    except Exception as e:
        print(f"  Error for tweet {tweet_id}: {str(e)[:100]}")
        return None

def main():
    input_file = r"C:\Users\nate8\Desktop\sna\data\raw\tweet_ids\tweetdata.txt"
    output_file = r"C:\Users\nate8\Desktop\sna\data\hydrated\tweetdata.jsonl"
    
    # Read tweet IDs
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            tweet_ids = [line.strip() for line in f if line.strip()]
        
        # PROCESS ONLY FIRST 1000 TWEETS FOR TESTING
        original_count = len(tweet_ids)
        tweet_ids = tweet_ids[:1000]  # <<< ADDED THIS LINE
        print(f"✓ Successfully read {original_count:,} tweet IDs from {input_file}")
        print(f"⚠️  PROCESSING ONLY FIRST 1,000 TWEETS FOR TESTING (out of {original_count:,})")
        
    except FileNotFoundError:
        print(f"✗ Error: Input file not found at {input_file}")
        print(f"  Please check the file exists and try again.")
        return
    except Exception as e:
        print(f"✗ Error reading file: {e}")
        return
    
    print(f"Starting hydration...")
    print("-" * 50)
    
    successful = 0
    failed = 0
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f_out:
        for i, tweet_id in enumerate(tweet_ids):
            print(f"[{i+1}/{len(tweet_ids)}] Processing {tweet_id}")
            
            tweet_data = get_tweet_data(tweet_id)
            
            if tweet_data:
                f_out.write(json.dumps(tweet_data, ensure_ascii=False) + "\n")
                successful += 1
                print(f"  ✓ Success")
            else:
                failed += 1
                print(f"  ✗ Failed")
            
            # Delay to avoid rate limiting - REDUCED FROM 1s to 0.2s FOR FASTER PROCESSING
            if i < len(tweet_ids) - 1:
                time.sleep(0.2)  # Changed from 1.0 to 0.2 seconds
    
    print("-" * 50)
    print(f"\nHYDRATION COMPLETE!")
    print(f"✓ Successful: {successful}")
    print(f"✗ Failed: {failed}")
    print(f"📁 Output saved to: {output_file}")
    
    # Show summary
    if successful > 0:
        print(f"\nTo view the first tweet:")
        print(f'  Get-Content "{output_file}" -First 1 | ConvertFrom-Json')

if __name__ == "__main__":
    main()