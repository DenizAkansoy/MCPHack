import asyncio
import random
from tweet_service import get_tweets, post_tweet
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client

from autogen import LLMConfig
from autogen.agentchat import AssistantAgent
from autogen.mcp import create_toolkit
import json
import anyio
import asyncio

import os
os.environ['OPENAI_API_KEY'] = '_'

# Only needed for Jupyter notebooks
import nest_asyncio
nest_asyncio.apply()

from autogen.agentchat.group import (
    AgentNameTarget,
    AgentTarget,
    AskUserTarget,
    ContextExpression,
    ContextStr,
    ContextStrLLMCondition,
    ContextVariables,
    ExpressionAvailableCondition,
    ExpressionContextCondition,
    GroupChatConfig,
    GroupChatTarget,
    Handoffs,
    NestedChatTarget,
    OnCondition,
    OnContextCondition,
    ReplyResult,
    RevertToUserTarget,
    SpeakerSelectionResult,
    StayTarget,
    StringAvailableCondition,
    StringContextCondition,
    StringLLMCondition,
    TerminateTarget,
)

from autogen.agentchat.group.patterns import (
    DefaultPattern,
    ManualPattern,
    AutoPattern,
    RandomPattern,
    RoundRobinPattern,
)


from autogen import ConversableAgent, UpdateSystemMessage
from autogen.agents.experimental import DocAgent
import os
import copy
from typing import Any, Dict, List
from pydantic import BaseModel, Field


from autogen.agentchat import initiate_group_chat, a_initiate_group_chat

import os
os.environ['OPENAI_API_KEY'] = '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'


async def find_funny_tweets_with_high_engagement():
    """Search for funny tweets with high engagement"""
    
    # Keywords likely to return funny content
    funny_keywords = [
        "funny joke",
        "comedy gold",
        "hilarious meme",
        "can't stop laughing",
        "funniest thing today",
        "comedy",
        "humor",
        "jokes",
        "lol funny"
    ]
    
    # Randomly select a search term
    search_term = random.choice(funny_keywords)
    print(f"Searching for: {search_term}")
    
    # Search for tweets with this term, sorting by 'Top' to get high engagement posts
    tweets = await get_tweets(query=search_term, sort_by='Top', count=20)
    
    if not tweets:
        print("No tweets found")
        return []
    
    # Calculate engagement score (likes + retweets + replies) for each tweet
    for tweet in tweets:
        tweet['engagement_score'] = tweet.get('likes', 0) + tweet.get('retweets', 0) + tweet.get('replies', 0)
    
    # Sort by engagement score
    high_engagement_tweets = sorted(tweets, key=lambda x: x.get('engagement_score', 0), reverse=True)
    
    # Print the top 5 tweets for reference
    print("\nTop 5 funny tweets with high engagement:")
    for i, tweet in enumerate(high_engagement_tweets[:5], 1):
        print(f"{i}. @{tweet.get('username')}: {tweet.get('text')[:100]}... " 
              f"(Engagement: {tweet.get('engagement_score')})")
    
    return high_engagement_tweets[:10]  # Return top 10 for inspiration

async def create_funny_tweet(inspiration_tweets):
    """Create a funny tweet based on trending topics in the inspiration tweets using an LLM agent"""
    
    # Format inspiration tweets for the prompt
    tweet_examples = []
    for tweet in inspiration_tweets[:5]:  # Use top 5 tweets
        text = tweet.get('text', '')
        username = tweet.get('username', 'unknown')
        engagement = tweet.get('engagement_score', 0)
        tweet_examples.append(f"@{username}: \"{text}\" (Engagement: {engagement})")
    
    # Create the system message for the LLM agent
    system_message = """
    You are a Twitter humor agent who creates funny, engaging tweets.
    
    Guidelines:
    - Create a short, funny tweet under 280 characters
    - Just be funny
    - Don't use overly complicated language
    """
    
    # Create the user message with examples and instructions
    user_message = f"""
    Below are popular funny tweets with high engagement. Use these as inspiration to create a new, original funny tweet.
    
    EXAMPLE TWEETS:
    {chr(10).join(tweet_examples)}
    
    Create ONE funny tweet that will get high engagement. Make it relatable and witty. Keep it under 280 characters.
    Only output the tweet text itself, no other text or explanations.
    """
    
    try:
        # Import the OpenAI client for v1.0.0+
        from openai import OpenAI
        
        # Initialize the client
        client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        
        # Call the API with the updated syntax
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            temperature=1.0,
            top_p=0.05,
            max_tokens=150
        )
        
        # Extract the content from the response
        tweet = response.choices[0].message.content.strip()
        
        # Make sure tweet is under 280 characters
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        
        print(f"LLM Agent generated tweet: {tweet}")
        return tweet
    
    except Exception as e:
        print(f"Error using LLM: {e}")
        
        # Use the original fallback but return as a string
        fallback = [
            "funny funny heheharhar"
        ]
        
        return fallback[0]

async def main():
    try:
        print("🔍 Looking for funny tweets with high engagement...")
        inspiration_tweets = await find_funny_tweets_with_high_engagement()
        
        print("\n✍️ Creating a funny tweet based on trending topics...")
        funny_tweet = await create_funny_tweet(inspiration_tweets)
        
        print(f"\n📝 Generated tweet: {funny_tweet}")
        
        # Ask for confirmation before posting
        confirm = input("\nDo you want to post this tweet? (y/n): ")
        if confirm.lower() == 'y':
            result = await post_tweet(text=funny_tweet)
            print(f"\n🚀 {result}")
        else:
            print("\n🛑 Tweet not posted.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())