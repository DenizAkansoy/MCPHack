import asyncio
from tweet_service import post_tweet

async def main():
    # Simple tweet content
    tweet_text = "Hello Twitter! This is a test tweet sent from my Python bot."
    
    try:
        # Post the tweet
        result = await post_tweet(text=tweet_text)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())