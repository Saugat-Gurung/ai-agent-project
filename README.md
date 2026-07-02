# Autonomous ReAct Agent Workflow: Multi-Agent Blogger

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Framework](https://img.shields.io/badge/Framework-Google%20ADK-orange)
![AI](https://img.shields.io/badge/Model-Gemini%201.5%20Flash-brightgreen)
![Status](https://img.shields.io/badge/Status-Production%20MVP-success)

## 📌 Project Overview
This project implements an autonomous, multi-agent artificial intelligence system using the **ReAct (Reasoning and Acting)** framework. Instead of relying on a single, linear LLM prompt, this architecture utilizes a microservices approach where specialized AI agents collaborate, evaluate, and iterate to generate production-ready technical content.

The current implementation acts as an automated technical documentation and blog pipeline, capable of researching a topic, structuring an outline, drafting content, and applying SEO/social media hooks without human intervention.

## 🏗️ System Architecture

The workflow is orchestrated by a **Root Agent** that delegates tasks to specialized sub-systems:
1. **The Planner Agent:** Generates a highly structured markdown outline based on the user's topic.
2. **The Writer Agent:** Ingests the validated outline from shared memory state and drafts a comprehensive, practical blog post targeting software engineers.
3. **The Orchestrator (Root):** Manages state handoffs, finalizes the output with metadata (e.g., alternative titles, Twitter hooks), and delivers the final payload.

## ⚙️ Technical Engineering Challenges Solved
Building reliable AI systems requires moving beyond happy-path scripting. This project specifically addresses several enterprise-level MLOps and infrastructure challenges:
* **API Rate Limiting (HTTP 429):** Mitigated `RESOURCE_EXHAUSTED` quotas by optimizing the execution graph, reducing unnecessary validation loops, and building a streamlined MVP pipeline to stay within strict 5 RPM constraints.
* **Server-Side Outages (HTTP 503):** Implemented understanding of model fallback routing to bypass high-traffic congestion on `latest` model endpoints.
* **Strict Type Validation:** Engineered the data payload to comply with strict Pydantic core validation, ensuring the SDK loop agents received correctly instantiated class objects rather than raw strings.
* **Filesystem & Dependency Management:** Utilized `uv` for high-speed, deterministic virtual environment resolution and managed hardlink volume constraints across partitioned drives.

## 📂 Folder Structure
```text
ai_agent_project/
├── .venv/                  # Isolated Python environment (managed via uv)
├── agent.py                # Core application logic and agent definitions
├── .env                    # Environment variables (API Keys - GitIgnored)
├── .gitignore              # Version control security guardrails
└── README.md               # System documentation

🚀 Quickstart & Installation
This project uses uv for lightning-fast dependency management.

1. Clone the repository and navigate to the directory:

Bash
git clone [https://github.com/yourusername/ai_agent_project.git](https://github.com/yourusername/ai_agent_project.git)
cd ai_agent_project

2. Create and activate the virtual environment:

Bash
uv venv .venv
# On Windows:
.\.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

3. Install dependencies:

Bash
uv pip install google-adk python-dotenv

4. Environment Configuration:
Create a .env file in the root directory and add your Google Gemini API key:

Plaintext
GOOGLE_API_KEY=your_api_key_here
MODEL_NAME=gemini-flash-latest


5. Launch the Application:
Run the following command to start the local ASGI server and open the web UI:

Bash
adk web

Navigate to http://127.0.0.1:8000 in your browser to interact with the agent workflow.
