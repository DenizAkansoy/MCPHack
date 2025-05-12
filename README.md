# InfoSys Cambridge Hackathon: Multi-Agent Study Assistant

Welcome to **MCPHack**, a collaborative agent-based tutor system built during the MCP Hackathon.

Give it **any study material** — class notes, a textbook snippet, a GitHub repo (e.g. *M2* or *S2* gitlab repo), or just any topic name like *"Photosynthesis"* or *"Lagrangian Mechanics"*. A team of intelligent agents will process the input to help you learn more effectively.

---

## What It Does

MCPHack simulates a **self-paced AI tutor** using multiple specialized agents. Given an input, the agents will:

- **Summarize** the core content
- **Enrich** it with external context (Wikipedia, arXiv, etc.)
- **Generate practice questions**
- **Evaluate your answers** and correct misconceptions
- **Explain concepts** through analogies and visuals
- **Track your learning progress** and suggest next topics

---

## Agent Roles

Each agent operates on a shared evolving context via the Model Context Protocol (MCP):

| Agent            | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `SummarizerAgent` | Condenses raw input into structured, digestible points                     |
| `ContextAgent`    | Expands the summary with relevant external sources or knowledge             |
| `QuestionAgent`   | Generates practice questions (MCQs, short answers, true/false)              |
| `CheckerAgent`    | Evaluates user answers and offers detailed corrections                     |
| `ExplainerAgent`  | Provides follow-up explanations, analogies, or visual aids                  |
| `ProgressAgent`   | Tracks what the user has learned and suggests what to study next            |


## Why This Matters

This project explores how Model Context Protocols can support **dynamic, modular, and interpretable AI systems** for education. Each agent can be reused, replaced, or extended independently.
