import argparse
from pathlib import Path
from typing import List, Dict
from newsapi import NewsApiClient
from mcp.server.fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("NewsServer")
NEWS_API_KEY= "8f2f3032f6754864a3768aad2413d7c3"

@mcp.tool()
def fetch_news(query: str, max_results: int = 3) -> List[str]:
    """
    Use the NewsAPI to fetch a news article based on the query.
    Returns a list of dictionaries with the article titles, published dates, and summaries.
    """
    # Replace 'YOUR_NEWSAPI_KEY' with your actual key.
    newsapi = NewsApiClient(api_key= NEWS_API_KEY)
    response = newsapi.get_everything(q=query, language='en', sort_by='relevancy', pageSize= max_results, page= 1)
    articles = response.get("articles", [])
    article_summaries= []
    if articles: 
        for article in articles:
            article_summaries.append(f"""
            title: {article.get("title", "No title")},
            date: {article.get("publishedAt", "No date")},
            summary: {article.get("description", "No summary")}"""
        )
        return article_summaries
    else:
        return [f"""
            title: No articles found,
            date: No date,
            summary: No summary """
        ]
    


