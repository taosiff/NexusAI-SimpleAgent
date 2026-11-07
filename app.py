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
    .badge-tavily { background-color: #FFF3E0; color: #E65100; }
    .badge-weather { background-color: #E1F5FE; color: #0288D1; }

    /* Tool Step Card */
    .step-card {
        background-color: #F7FAFC;
        border-left: 4px solid #4A90E2;
        padding: 10px 14px;
        margin-bottom: 8px;
        border-radius: 4px;
        font-size: 0.88rem;
    }
    .step-tool {
        font-weight: 700;
        color: #2D3748;
    }
</style>
""", unsafe_allow_html=True)

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
    temperature = st.slider("Model Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.1, help="Lower = more deterministic; Higher = more creative.")
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
    "<div class='sub-title'>An autonomous ReAct agent powered by <b>Google Gemini 3.5</b> and <b>LangChain</b> capable of multi-step reasoning, real-time web search, and live weather tracking.</div>",
    unsafe_allow_html=True
)

# --- Load & Sync API Keys (Supports os.environ, st.secrets, and aliases) ---
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

if missing_keys:
    st.warning(f"⚠️ Missing environment variables: `{', '.join(missing_keys)}`. Please check your deployment settings.")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am **NexusAI**, an autonomous AI agent. I can perform live web searches, look up real-time global weather, and reason across multiple steps to answer complex inquiries. How can I help you today?"
        }
    ]

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "steps" in message and message["steps"]:
            with st.expander("🔍 View Agent Thought Process & Tool Steps"):
                for action, observation in message["steps"]:
                    st.markdown(f"**Action:** `{action.tool}`")
                    st.markdown(f"**Input:** `{action.tool_input}`")
                    st.markdown(f"**Observation:**\n```\n{observation}\n```")
                    st.markdown("---")

# Handle User Input (via chat input or sidebar quick prompt)
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
        with st.status("🧠 NexusAI is reasoning & querying tools...", expanded=True) as status_box:
            try:
                executor = get_agent_executor(
                    max_search_results=max_search_results,
                    temperature=temperature
                )
                
                response = executor.invoke({"input": user_prompt})
                output_text = response.get("output", "No response generated.")
                steps = response.get("intermediate_steps", [])

                # Render intermediate reasoning in the status widget
                if steps:
                    for i, (action, observation) in enumerate(steps, 1):
                        st.write(f"**Step {i}: Using Tool** `{action.tool}`")
                        st.code(f"Input: {action.tool_input}\nResult: {str(observation)[:300]}...", language="text")
                else:
                    st.write("Direct reasoning without external tools.")

                status_box.update(label="✅ Task Completed!", state="complete", expanded=False)

                # Render final markdown answer
                st.markdown(output_text)

                # Save to session history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": output_text,
                    "steps": steps
                })

            except Exception as e:
                status_box.update(label="❌ Execution Error", state="error", expanded=True)
                st.error(f"Error during execution: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"⚠️ An error occurred while executing your request: `{str(e)}`"
                })

