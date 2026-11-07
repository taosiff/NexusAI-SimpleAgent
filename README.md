# ⚡ NexusAI — Autonomous Multi-Tool Intelligence Agent

[![Live Demo on Render](https://img.shields.io/badge/Live%20Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://nexusai-simpleagent.onrender.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-3.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An enterprise-ready **autonomous AI Agent** built with **LangChain** and powered by **Google Gemini 3.5 Flash**. The agent implements the **ReAct (Reasoning + Acting)** paradigm to dynamically reason through multi-step inquiries, utilize specialized real-time tools, remember conversation context via memory buffers, and present transparent decision-making through a modern, responsive **Streamlit** user interface.

🌐 **Try the Live Application:**  
👉 **[https://nexusai-simpleagent.onrender.com/](https://nexusai-simpleagent.onrender.com/)**

> [!NOTE]
> **Free-Tier Developer Quotas & Rate Limits:**  
> This public demo is hosted on free cloud tiers and connects to free developer API accounts (Google AI Studio, Tavily Search, and Weatherstack). If you occasionally see a rate limit or quota notice, it is because public visitors have temporarily exhausted the free-tier requests. If that happens, feel free to clone this repository, insert your own free API keys, and run it locally without restrictions!

---

## 🌟 Key Features

- 🧠 **Autonomous ReAct Agent Reasoning**: Employs the Thought-Action-Observation cycle to decompose multi-part user requests into discrete, executable steps.
- 💾 **Conversational Memory**: Retains multi-turn conversation context across interactions using LangChain's `ConversationBufferMemory`.
- 🔍 **Real-Time Web Intelligence**: Leverages the **Tavily Search API** for up-to-the-minute web retrieval and breaking news beyond model knowledge cutoffs.
- 🌦️ **Live Meteorological Telemetry**: Connects with the **Weatherstack API** to retrieve live temperature, wind speed, condition, humidity, and "feels-like" metrics globally.
- 🛡️ **Fault-Tolerant Execution**: Features built-in `handle_parsing_errors=True` self-correction, resilient JSON parameter sanitization, and offline prompt fallbacks.
- 📊 **Step Transparency**: The interactive Streamlit UI reveals the agent's internal thought process and intermediate tool results in real time.
- 🚀 **Zero-Cost Deployment**: Built entirely on free-tier APIs and deployed on **Render** (also supports 1-click deployment on **Streamlit Community Cloud**).

---

## 🏗️ System Architecture

```text
       ┌────────────────────────┐
       │   User / Streamlit UI  │
       └───────────┬────────────┘
                   │ (User Query + Conversation History)
                   ▼
       ┌────────────────────────┐
       │  ReAct Agent Executor  │ ◄─────── LangChain Hub
       └───────────┬────────────┘          (ReAct Prompt Template)
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
┌─────────────────┐ ┌───────────────────────────────┐
│  Google Gemini  │ │       Tool Invocations        │
│   3.5 Flash     │ │                               │
└────────┬────────┘ │  • 🔍 Tavily Search API       │
         │          │     (Live Web Search)         │
         │ (Decides │                               │
         │  Action) │  • 🌦️ Weatherstack API        │
         │          │     (Live Global Weather)     │
         │          └───────────────┬───────────────┘
         │                          │
         ▼ (Synthesizes Observation)▼
       ┌────────────────────────┐
       │     Final Response     │
       └───────────┬────────────┘
                   │ (Updates Memory Buffer)
                   ▼
       ┌────────────────────────┐
       │ ConversationBuffer     │
       │ Memory (Session State) │
       └────────────────────────┘
```

---

## 📁 Repository Structure

```text
├── app.py                  # Streamlit web UI with interactive agent dashboard
├── main.py                 # Core AI agent logic, tools, memory, and execution engine
├── requirements.txt        # Pinned dependencies for reproducible cloud deployment
├── .env.example            # Environment variables configuration template
├── .gitignore              # Protects secrets (.env) and virtual environments
└── Code step by step/      # Interactive Jupyter notebook for prototyping & learning
    ├── code.ipynb          # Step-by-step notebook tutorial
    └── .env                # Local development credentials (git-ignored)
```

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/taosiff/NexusAI-SimpleAgent.git
cd NexusAI-SimpleAgent
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```
Inside `.env`:
```env
GOOGLE_API_KEY="your_google_ai_studio_key"
TAVILY_API_KEY="your_tavily_api_key"
WEATHERSTACK_API_KEY="your_weatherstack_api_key"
```

> **Where to get keys for free:**
> - [Google AI Studio (Gemini)](https://aistudio.google.com/) — Free tier, no credit card.
> - [Tavily Search](https://tavily.com/) — 1,000 free API queries/month.
> - [Weatherstack](https://weatherstack.com/) — Free tier forever.

### 5. Run the Application
```bash
streamlit run app.py
```
Visit `http://localhost:8501` in your browser.

---

## 🌐 Cloud Deployment

### Option A: Render (Current Live Deployment)
1. Create a new **Web Service** on [Render](https://render.com) connected to your GitHub repo.
2. Settings:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
3. Under **Environment Variables**, add:
   - `GOOGLE_API_KEY`
   - `TAVILY_API_KEY`
   - `WEATHERSTACK_API_KEY`

### Option B: Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io/) and select your repository.
2. Set **Main file path** to `app.py`.
3. In **Advanced Settings ➔ Secrets**, paste your API keys in TOML format and click **Deploy**.

---

## 👨‍💻 Tech Stack & Integrations

- **LLM Core:** Google Gemini 3.5 Flash
- **Agent Orchestration:** LangChain (ReAct framework + Memory)
- **Web Retrieval:** Tavily Search Python SDK
- **Weather Telemetry:** Weatherstack REST API
- **Frontend / UI:** Streamlit
- **Deployment Platform:** Render

---

## 📄 License

This project is open-source and licensed under the [MIT License](LICENSE).
