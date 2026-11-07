# ⚡ NexusAI — Autonomous Multi-Tool Intelligence Agent

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-3.5%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://aistudio.google.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An enterprise-ready **autonomous AI Agent** built with **LangChain** and powered by **Google Gemini 3.5 Flash**. The agent implements the **ReAct (Reasoning + Acting)** paradigm to dynamically reason through multi-step inquiries, utilize specialized real-time tools, and present transparent decision-making through a modern, responsive **Streamlit** user interface.

---

## 🌟 Key Features

- 🧠 **Autonomous ReAct Agent Reasoning**: Employs the Thought-Action-Observation cycle to decompose multi-part user requests into discrete, executable steps.
- 🔍 **Real-Time Web Intelligence**: Leverages the **Tavily Search API** for up-to-the-minute web retrieval and breaking news beyond model knowledge cutoffs.
- 🌦️ **Live Meteorological Telemetry**: Connects with the **Weatherstack API** to retrieve live temperature, wind speed, condition, humidity, and "feels-like" metrics globally.
- 🛡️ **Fault-Tolerant Execution**: Features built-in `handle_parsing_errors=True` self-correction, resilient JSON parameter sanitization, and offline prompt fallbacks.
- 📊 **Step Transparency**: The interactive Streamlit UI reveals the agent's internal thought process and intermediate tool results in real time.
- 🚀 **Zero-Cost Deployment**: Built entirely on free-tier APIs and ready for 1-click deployment to **Streamlit Community Cloud**.

---

## 🏗️ System Architecture

```text
       ┌────────────────────────┐
       │   User / Streamlit UI  │
       └───────────┬────────────┘
                   │ (User Query)
                   ▼
       ┌────────────────────────┐
       │  ReAct Agent Executor  │ ◄─────── LangChain Hub
       └───────────┬────────────┘          (ReAct Prompt)
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
┌─────────────────┐ ┌─────────────────┐
│  Google Gemini  │ │ Tool Invocation │
│   3.5 Flash     │ │      Logic      │
└────────┬────────┘ └────────┬────────┘
         │ (Decides Action)  │
         │                   ├────────► 🔍 Tavily Search API
         │                   │           (Live Web Search)
         │                   │
         │                   └────────► 🌦️ Weatherstack API
         │                               (Live Global Weather)
         ▼ (Synthesizes Observation)
       ┌────────────────────────┐
       │     Final Response     │
       └────────────────────────┘
```

---

## 📁 Repository Structure

```text
├── app.py                  # Streamlit web UI with interactive agent dashboard
├── main.py                 # Core AI agent logic, tools, and execution engine
├── requirements.txt        # Pinned dependencies for reproducible deployment
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
git clone https://github.com/YOUR_USERNAME/NexusAI-Agent.git
cd NexusAI-Agent
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

## 🌐 1-Click Deployment (Streamlit Community Cloud)

You can deploy this project live for free in under 3 minutes:

1. Push your code to your **GitHub repository** (ensure `.env` is NOT pushed).
2. Go to **[share.streamlit.io](https://share.streamlit.io/)** and sign in with GitHub.
3. Click **"New app"**:
   - **Repository:** `YOUR_USERNAME/NexusAI-Agent`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Expand **Advanced Settings → Secrets** and add your keys:
   ```toml
   GOOGLE_API_KEY = "your_google_key"
   TAVILY_API_KEY = "your_tavily_key"
   WEATHERSTACK_API_KEY = "your_weatherstack_key"
   ```
5. Click **"Deploy!"** — your agent is now live with a public URL you can share with recruiters and on LinkedIn!

---

## 👨‍💻 Tech Stack & Integrations

- **LLM Core:** Google Gemini 3.5 Flash
- **Agent Orchestration:** LangChain (ReAct framework)
- **Web Retrieval:** Tavily Search Python SDK
- **Weather Telemetry:** Weatherstack REST API
- **Frontend / UI:** Streamlit
- **Environment Management:** python-dotenv

---

## 📄 License

This project is open-source and licensed under the [MIT License](LICENSE).

