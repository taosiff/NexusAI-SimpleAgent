"""
app.py - Sleek Streamlit Web Interface for NexusAI Agent
"""

import os
import streamlit as st
from main import get_agent_executor

# --- Page Configuration ---
st.set_page_config(
    page_title="NexusAI | Autonomous Intelligence Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
<style>
    /* Global Styles */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4A90E2, #9013FE);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1rem;
        color: #718096;
        margin-bottom: 25px;
    }
    .badge {
        display: inline-block;
        padding: 3px 8px;
        font-size: 11px;
        font-weight: 600;
        border-radius: 6px;
        margin-right: 6px;
    }
    .badge-gemini { background-color: #E8F0FE; color: #1967D2; }
    .badge-langchain { background-color: #EEFBE7; color: #1E7E34; }

    /* Tool Step Card */
    .step-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #3B82F6;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 12px;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# --- Load & Sync API Keys ---
for k in ["GOOGLE_API_KEY", "GEMINI_API_KEY", "TAVILY_API_KEY", "WEATHERSTACK_API_KEY"]:
    v = None
    try:
        if hasattr(st, "secrets") and k in st.secrets:
            v = str(st.secrets[k])
    except Exception:
        pass
    if not v and os.getenv(k):
        v = os.getenv(k)

    if v:
        clean_v = v.strip().strip("'").strip('"')
        os.environ[k] = clean_v
        if k == "GEMINI_API_KEY" and "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = clean_v

google_key = os.getenv("GOOGLE_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")
weather_key = os.getenv("WEATHERSTACK_API_KEY")

missing_keys = []
if not google_key: missing_keys.append("GOOGLE_API_KEY")
if not tavily_key: missing_keys.append("TAVILY_API_KEY")
if not weather_key: missing_keys.append("WEATHERSTACK_API_KEY")

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown("### ⚡ NexusAI Agent")
    st.markdown(
        "<span class='badge badge-gemini'>Google Gemini 3.5</span>"
        "<span class='badge badge-langchain'>LangChain</span>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    
    st.markdown("#### 🛠️ Active Tools")
    st.markdown("- 🔍 **Tavily Search**: Real-time web retrieval & breaking news")
    st.markdown("- 🌦️ **Weatherstack API**: Live global weather conditions")
    
    st.markdown("---")
    st.markdown("#### ⚙️ Settings")
    temperature = st.slider("Model Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.1, help="Lower = strict & factual; Higher = creative.")
    max_search_results = st.slider("Max Search Results", min_value=1, max_value=5, value=2)

    st.markdown("---")
    st.markdown("#### 💡 Quick Prompts")
    prompt_options = [
        "What is the capital of Bangladesh and what is the current weather there?",
        "What are the latest updates on the 2026 US midterm elections?",
        "Compare the current weather in Tokyo and Paris.",
        "What are the top AI breakthroughs in robotics this month?"
    ]
    
    for p in prompt_options:
        if st.button(p, use_container_width=True):
            st.session_state["queued_prompt"] = p

    st.markdown("---")
    if st.button("🧹 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("queued_prompt", None)
        st.rerun()

    st.caption("Developed with ❤️ using Python, LangChain & Streamlit.")


# --- Main Application Header ---
st.markdown("<div class='main-title'>⚡ NexusAI Intelligence Agent</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-title'>An autonomous ReAct agent powered by <b>Google Gemini 3.5</b> and <b>LangChain</b> with transparent reasoning, real-time web search, and live weather tracking.</div>",
    unsafe_allow_html=True
)

if missing_keys:
    st.warning(f"⚠️ Missing environment variables: `{', '.join(missing_keys)}`. Please check your deployment settings.")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am **NexusAI**, an autonomous AI agent. I can perform live web searches, check real-time global weather, and reason across multiple steps to answer complex inquiries. How can I help you today?",
            "steps": []
        }
    ]


def render_steps(steps):
    """Renders agent tool steps openly without hiding them."""
    valid_steps = [s for s in steps if s[0].tool != "_Exception"]
    if not valid_steps:
        return
    
    st.markdown("##### 🧠 Agent Tool Executions")
    for i, (action, observation) in enumerate(valid_steps, 1):
        tool_name = "Tavily Web Search" if "tavily" in action.tool.lower() else "Weatherstack API" if "weather" in action.tool.lower() else action.tool
        with st.container():
            st.markdown(f"""
            <div class="step-box">
                <b>Step {i}: Invoked <code>{tool_name}</code></b><br>
                <b>Input:</b> <code>{action.tool_input}</code><br>
                <b>Observation:</b><br>
                <pre style="white-space: pre-wrap; font-size: 12px; margin-top: 5px;">{str(observation).strip()}</pre>
            </div>
            """, unsafe_allow_html=True)


# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "steps" in message and message["steps"]:
            render_steps(message["steps"])
        st.markdown(message["content"])

# --- Handle User Input ---
user_prompt = st.chat_input("Ask a question or request an action...")
if "queued_prompt" in st.session_state and st.session_state["queued_prompt"]:
    user_prompt = st.session_state.pop("queued_prompt")

if user_prompt:
    # 1. Display User Message
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # 2. Execute Agent
    with st.chat_message("assistant"):
        thought_placeholder = st.empty()
        thought_placeholder.info("🧠 **NexusAI is analyzing your request and determining necessary tools...**")

        try:
            executor = get_agent_executor(
                max_search_results=max_search_results,
                temperature=temperature
            )
            
            response = executor.invoke({"input": user_prompt})
            output_text = response.get("output", "No response generated.")
            steps = response.get("intermediate_steps", [])

            # Clear temporary thinking banner
            thought_placeholder.empty()

            # Render all reasoning and tool calls visibly
            if steps:
                render_steps(steps)

            # Render final answer prominently
            st.markdown(output_text)

            # Save to history
            st.session_state.messages.append({
                "role": "assistant",
                "content": output_text,
                "steps": steps
            })

        except Exception as e:
            thought_placeholder.empty()
            st.error(f"Error during execution: {str(e)}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"⚠️ An error occurred while executing your request: `{str(e)}`",
                "steps": []
            })
