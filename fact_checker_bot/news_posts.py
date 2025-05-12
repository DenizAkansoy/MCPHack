import asyncio
import random
from tweet_service import get_tweets, post_tweet
import os

os.environ['OPENAI_API_KEY'] = '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'  # Replace with your actual API key
num_tweets = 20

async def find_latest_news_tweets():
    """Search for the latest news tweets"""
    
    # Keywords likely to return news content
    news_keywords = [
        "breaking news",
        "latest news",
        "news update",
        "headline",
        "news",
        "current events",
        "just now",
        "happened"
    ]
    
    # Randomly select a search term
    search_term = random.choice(news_keywords)
    print(f"Searching for: {search_term}")
    
    # Search for tweets with this term, sorting by 'Latest' to get recent posts
    tweets = await get_tweets(query=search_term, sort_by='Latest', count=num_tweets)
    
    if not tweets:
        print("No tweets found")
        return []
    
    # Print the top 5 latest news tweets for reference
    print("\nTop 5 latest news tweets:")
    for i, tweet in enumerate(tweets[:5], 1):
        print(f"{i}. @{tweet.get('username')}: {tweet.get('text')[:100]}...")
    
    return tweets[:10]  # Return top 10 for further use


async def main():
    try:
        print("🔍 Looking for the latest news tweets...")
        inspiration_tweets = await find_latest_news_tweets()
        
        return inspiration_tweets
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())