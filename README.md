# AgenticAI_Buddy
Agentic AI based multi-agent application. 
This handles users' queries on specific topics related to Finance, Career, Health and Travel, Math and Coding.

### Agents:
- AIBuddy - main agent/triage agent
Following are specialized agents for domain specific queries:
- FinanceBuddy
- CareerBuddy
- HealthBuddy
- TravelBuddy
- MathandCodingBuddy

(The current version I have implemented & pushed here works. But it is still a work in progress as I will further enhance it with code refactoring, better UI and improve multi-agent orchestration.)

### Tools used:
- OpenAI Agents SDK
- FAISS - Vector index/search (for RAG)
- Streamlit - UI

Here I used the following related concepts: <br>
✅ Agentic Handoff <br>
✅ Tool integration: eg: Web search, Function calling. <br>
✅ Agent as tool (e.g.: using Wealth buddy as a financial planning tool for  TravelBuddyAgents Trip Budgeting.)<br>
✅ RAG (Retrieval augmented generation): provides additional context for the LLM. 

Let me summarize the various concepts I explored:

- Agents: these are LLMs that are capable of doing specialized tasks and can incorporate various tools to get a task done.

- Handoff: This is redirecting the request to a specific agent. This way, we can build and delegate user instructions to specialized agents.

- Tool integration: Agents SDK provides various tool integrations such as Websearch, Filesearch, Image generation tool, Localshell tool, Function tool, to name a few.
With tool integration such as Websearch or Function tool, the agent can perform web searches or use our custom functions, respectively. 

- RAG: RAG is used to enhance the quality of the responses by augmentating the  LLM's knowledge by relevant context. In simpler words, think of it as an open book exam.  To implement this, I used vector search retrieval to retrieve context from past questions and responses which we refer as the knowledge base. This context can be used by the Agent to respond appropriately to the user. For this I have used FAISS to index the knowledge base. 
