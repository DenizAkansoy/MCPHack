# InfoSys Cambridge Hackathon: Multi-Agent Fact-Checking for Social Media

**FactCheckBot** is a multi-agent system designed to identify, verify, and respond to factual claims on social media platforms like Twitter (X). Built using the **Model Context Protocol (MCP)**, the system decomposes the complex task of fact-checking into modular, intelligent agents — each responsible for a specific decision or reasoning step.

---

## What It Does

Given a tweet or thread, FactCheckBot:

1. Extracts factual claims
2. Searches reliable external sources
3. Evaluates the claim based on supporting or contradicting evidence
4. Falls back on crowdsourced consensus for recent events
5. Generates a concise, explainable verdict
6. Posts a correction or clarification as a reply

This system is designed to combat misinformation with speed, context, and transparency.

---

## Agent Roles

| Agent Name           | Description |
|----------------------|-------------|
| `ClaimExtractorAgent` | Detects and isolates factual claims from tweets |
| `RetrieverAgent`      | Searches verified sources (Wikipedia, arXiv, news APIs, etc.) |
| `VerifierAgent`       | Compares the claim to retrieved evidence and makes an initial judgment |
| `CrowdSignalAgent`    | In breaking news cases, checks for regional consensus across social media |
| `ExplainerAgent`      | Summarizes the verdict in human-readable language, with reasoning |
| `PosterAgent`         | Posts a reply to the original tweet, including sources and explanations |

All agents operate on a shared memory structure defined by the **Model Context Protocol**, allowing dynamic coordination and context-aware reasoning.

---

## Example Workflow

### Input Tweet:
> “Massive explosion reported in Ankara right now.”

### Agent Flow:
1. `ClaimExtractorAgent` detects a location-based factual claim.
2. `RetrieverAgent` finds **no results** in verified sources — too recent.
3. `CrowdSignalAgent` clusters 10+ independent geolocated users in Ankara posting similar claims.
4. `VerifierAgent` assigns a **tentative credibility score** with fallback reasoning.
5. `ExplainerAgent` formats the reply:
   > “🚨 Developing: This event is not yet reported by major outlets, but multiple users in Ankara are sharing photos and consistent details. Treat as likely true, pending confirmation. [Context]”
6. `PosterAgent` publishes the reply.

---

## Real-Time Consensus via CrowdSignalAgent

In cases where a claim cannot be confirmed through traditional sources (e.g., breaking news or remote events), the system uses **CrowdSignalAgent** to:

- Search for tweets matching the claim
- Filter for **geolocated**, **domain-relevant**, or **independent** sources
- Evaluate consensus within a time window
- Provide a **fallback credibility score** if traditional verification is unavailable

This helps prevent **false negatives** and enhances trustworthiness in time-sensitive cases.

---
