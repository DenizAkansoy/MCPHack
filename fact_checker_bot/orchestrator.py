# factcheck_orchestrator.py

import asyncio
from datetime import datetime
from autogen import ConversableAgent, Agent
from ag2.context import Context, ContextVariables, ContextStr
from autogen.agentchat.group import (
    AgentTarget,
    OnContextCondition,
    TerminateTarget,
    DefaultPattern,
    a_initiate_group_chat
)
from tweet_service import get_tweets, post_tweet

# --- Orchestrator Agent ---
class OrchestratorAgent(Agent):
    def run(self, context: Context) -> Context:
        search_context = context.get("search_context")
        verdict = context.get("verdict")
        sources = context.get("retrieved_sources", [])
        used_crowd = context.get("used_crowd_signal", False)
        confidence = context.get("confidence_score", 0.0)

        if verdict:
            if "false" in verdict.lower():
                confidence = 0.95
            elif len(sources) >= 2:
                confidence = 0.85
            elif len(sources) == 1:
                confidence = 0.65
            else:
                confidence = 0.4

        context["confidence_score"] = confidence

        if confidence < 0.6 and not used_crowd:
            context["next_agent"] = "crowd_signal"
        elif verdict:
            context["next_agent"] = "explainer"
        else:
            context["next_agent"] = "search_context_agent"

        return context

# --- Search Context Extractor Agent using OpenAI ---
from autogen.agents.tool import register_function

@register_function
def generate_search_context(tweet_text: str) -> str:
    """
    Given a tweet, extract a short query or keyword list that best captures the event or topic
    for use in news search. Use OpenAI's language understanding to summarize the key context.
    """
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"""
    Extract a concise query or keyword list that best represents the key information in this tweet
    for use in searching news sources. Keep it short and focused on relevant names, places, and events.

    Tweet: "{tweet_text}"
    Query:
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=50
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return f"Error generating context: {e}"

search_context_agent = ConversableAgent(
    name="search_context_agent",
    system_message="Use the generate_search_context tool to extract a focused query from the tweet for searching news.",
    llm_config={
        'functions': [generate_search_context],
        'function_call': {'name': 'generate_search_context'}
    }
)

retriever = ConversableAgent(
    name="retriever",
    system_message="Use the search_context to search for related news and summarize the results."
)

verifier = ConversableAgent(
    name="verifier",
    system_message="Given the sources and the tweet, evaluate the truthfulness and return a verdict."
)

crowd_signal = ConversableAgent(
    name="crowd_signal",
    system_message="Estimate support for the claim by checking if multiple users posted about it. Set 'used_crowd_signal': True"
)

explainer = ConversableAgent(
    name="explainer",
    system_message="Generate a tweet-size explanation of the verdict and why it was reached."
)

poster = ConversableAgent(
    name="poster",
    system_message="Post the tweet using the post_tweet tool."
)

# --- Handoffs ---
orchestrator = OrchestratorAgent(name="orchestrator")
orchestrator.handoffs.add_context_conditions([
    OnContextCondition(ContextStr("next_agent == 'crowd_signal'"), AgentTarget(crowd_signal)),
    OnContextCondition(ContextStr("next_agent == 'explainer'"), AgentTarget(explainer)),
    OnContextCondition(ContextStr("next_agent == 'search_context_agent'"), AgentTarget(search_context_agent)),
])

search_context_agent.handoffs.set_after_work(AgentTarget(retriever))
retriever.handoffs.set_after_work(AgentTarget(verifier))
verifier.handoffs.set_after_work(AgentTarget(orchestrator))
crowd_signal.handoffs.set_after_work(AgentTarget(orchestrator))
explainer.handoffs.set_after_work(AgentTarget(poster))
poster.handoffs.set_after_work(TerminateTarget())

# --- Main pipeline to run over live tweets ---
async def run_factchecker_pipeline():
    print("🔍 Searching Twitter for recent breaking news...")
    tweets = await get_tweets(query="breaking news", sort_by="Latest", count=10)

    for tweet in tweets:
        tweet_text = tweet.get("text")
        timestamp = datetime.utcnow().isoformat()
        print(f"\n🧵 Fact-checking tweet: {tweet_text[:80]}...")

        context = ContextVariables(data={
            "tweet_text": tweet_text,
            "timestamp": timestamp
        })

        pattern = DefaultPattern(
            agents=[
                search_context_agent,
                retriever,
                verifier,
                crowd_signal,
                orchestrator,
                explainer,
                poster,
            ],
            initial_agent=search_context_agent,
            context_variables=context,
        )

        await a_initiate_group_chat(
            pattern=pattern,
            messages="Fact-check this tweet",
            max_rounds=15
        )

if __name__ == "__main__":
    asyncio.run(run_factchecker_pipeline())
