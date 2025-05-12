import asyncio
import random
from tweet_service import get_tweets, post_tweet

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
    """Create a funny tweet based on trending topics in the inspiration tweets"""
    if not inspiration_tweets:
        return "Just had a thought - why do we drive on parkways and park on driveways? #RandomThoughts #FunnyObservations"
    
    # Extract topics and themes from the inspiration tweets
    all_text = " ".join([tweet.get('text', '') for tweet in inspiration_tweets])
    
    # Simple templates for funny tweets
    funny_templates = [
        "That moment when {topic} and you just can't even... 😂 #FunnyThoughts",
        "Pro tip: Never {action} when you're {situation}. Learned this the hard way! 🤣 #LifeLessons",
        "Is it just me or is {topic} getting more ridiculous every day? #JustSaying #LOL",
        "My relationship with {topic} is complicated. It's mostly me {action} and {topic} ignoring me. #FunnyButTrue",
        "Breaking news: Scientists discover that {topic} is actually just {alternative}. Everyone is shocked. #MindBlown",
        "Life hack: Instead of {normal_action}, try {silly_action}. Works 60% of the time, every time! #LifeHacks #Comedy",
        "This is your daily reminder that {obvious_fact}. You're welcome. #PSA #Humor",
        "Plot twist: {unexpected_scenario}. Nobody saw that coming! #PlotTwist #Funny",
        "Today's goal: {simple_task}. Today's reality: {disaster_scenario}. #RelateableTruths"
    ]
    
    # Fun topics we can use if we can't extract something good
    fallback_topics = [
        "social media addiction", "adulting", "Monday mornings", 
        "autocorrect fails", "online shopping", "working from home",
        "diet plans", "technology", "dating apps", "coffee dependency",
        "streaming services", "food delivery", "weather forecasts"
    ]
    
    # Potential actions for templates
    actions = [
        "scrolling endlessly", "overthinking", "procrastinating", 
        "online shopping", "binge-watching", "dancing", "cooking",
        "sending texts", "taking selfies", "making decisions"
    ]
    
    # Potential situations
    situations = [
        "sleep-deprived", "hungry", "caffeinated", "in a meeting",
        "supposed to be working", "trying to impress someone", 
        "already late", "on a diet", "in public"
    ]
    
    # Try to extract trending topics from inspiration tweets, or use fallbacks
    trending_topics = []
    for tweet in inspiration_tweets:
        text = tweet.get('text', '').lower()
        # Skip retweets and very short content
        if text.startswith('rt @') or len(text) < 20:
            continue
        
        # Extract potential topic phrases (this is simplified)
        words = text.split()
        if len(words) > 3:
            # Take a random 2-3 word phrase from the middle of the tweet
            start_idx = random.randint(0, len(words) - 3)
            phrase_length = random.randint(2, 3)
            phrase = " ".join(words[start_idx:start_idx + phrase_length])
            if len(phrase) > 5 and not phrase.startswith('@') and not phrase.startswith('#'):
                trending_topics.append(phrase)
    
    # If we couldn't extract good topics, use fallbacks
    if not trending_topics:
        trending_topics = fallback_topics
    
    # Choose template and fill in the placeholders
    template = random.choice(funny_templates)
    
    if "{topic}" in template:
        template = template.replace("{topic}", random.choice(trending_topics))
    
    if "{action}" in template:
        template = template.replace("{action}", random.choice(actions))
        
    if "{situation}" in template:
        template = template.replace("{situation}", random.choice(situations))
        
    if "{normal_action}" in template:
        normal_actions = ["waking up early", "doing laundry", "making plans", "cooking dinner"]
        template = template.replace("{normal_action}", random.choice(normal_actions))
        
    if "{silly_action}" in template:
        silly_actions = ["sleeping in", "buying new clothes", "canceling last minute", "ordering takeout"]
        template = template.replace("{silly_action}", random.choice(silly_actions))
        
    if "{obvious_fact}" in template:
        obvious_facts = ["pizza is better than salad", "naps are underrated", "mondays are the worst", "chocolate fixes everything"]
        template = template.replace("{obvious_fact}", random.choice(obvious_facts))
        
    if "{unexpected_scenario}" in template:
        scenarios = [
            "your plants are judging your life choices",
            "your coffee maker is secretly plotting against you",
            "your cat has been writing a novel about you",
            "your phone is only pretending to need charging"
        ]
        template = template.replace("{unexpected_scenario}", random.choice(scenarios))
        
    if "{simple_task}" in template and "{disaster_scenario}" in template:
        tasks = ["answer one email", "go to bed early", "drink more water", "organize one drawer"]
        disasters = ["inbox now at 1,457 unread", "it's 3 AM and I'm on my fifth episode", "spilled water all over my laptop", "entire house now in chaos"]
        template = template.replace("{simple_task}", random.choice(tasks))
        template = template.replace("{disaster_scenario}", random.choice(disasters))
        
    if "{alternative}" in template:
        alternatives = ["a conspiracy theory", "three kids in a trenchcoat", "completely optional", "actually cake"]
        template = template.replace("{alternative}", random.choice(alternatives))
    
    # Add some emoji for good measure
    emojis = ["😂", "🤣", "😅", "😆", "🙃", "🤦‍♀️", "🤷‍♂️", "💯", "👀", "🔥"]
    if random.random() > 0.5 and not any(emoji in template for emoji in emojis):
        template += f" {random.choice(emojis)}"
    
    return template

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