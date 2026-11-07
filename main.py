"""
main.py - Core AI Agent Engine
Built with LangChain, Google Gemini, Tavily Search, and Weatherstack API.
"""

import os
import re
import json
import certifi
import requests
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor

# Configure SSL certificate path
os.environ["SSL_CERT_FILE"] = certifi.where()

# Load environment variables
load_dotenv(override=True)


def parse_city_input(city_input) -> str:
    """Helper to extract clean city name from various agent input formats."""
    if isinstance(city_input, dict):
        return city_input.get("city", str(city_input))
    
    city_str = str(city_input).strip()
    if city_str.startswith("{") and city_str.endswith("}"):
        try:
            parsed = json.loads(city_str)
            if isinstance(parsed, dict):
                return parsed.get("city", list(parsed.values())[0])
        except Exception:
            pass
            
    city_str = re.sub(r'[\'"{}]', '', city_str).strip()
    return city_str


@tool
def get_weather_data(city: str) -> str:
    """Fetch current real-time weather information for any given city."""
    api_key = os.getenv("WEATHERSTACK_API_KEY")
    if not api_key or api_key == "your_weatherstack_api_key_here":
        return "Error: WEATHERSTACK_API_KEY is not configured in environment variables."

    clean_city = parse_city_input(city)
    url = f"https://api.weatherstack.com/current?access_key={api_key}&query={clean_city}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if "current" not in data:
            error_info = data.get("error", {}).get("info", "Unknown error")
            return f"Could not fetch weather data for '{clean_city}'. Reason: {error_info}"

        location = data.get("location", {})
        current = data.get("current", {})
        city_name = location.get("name", clean_city)
        country = location.get("country", "")

        return (
            f"Weather in {city_name}, {country}:\n"
            f"- Temperature: {current.get('temperature')}°C\n"
            f"- Condition: {current.get('weather_descriptions', ['N/A'])[0]}\n"
            f"- Humidity: {current.get('humidity')}%\n"
            f"- Wind Speed: {current.get('wind_speed')} km/h\n"
            f"- Feels Like: {current.get('feelslike')}°C"
        )
    except requests.exceptions.RequestException as e:
        return f"Network error fetching weather data for '{clean_city}': {str(e)}"


def get_agent_executor(max_search_results: int = 3, temperature: float = 0.0) -> AgentExecutor:
    """
    Initializes and returns the complete ReAct AgentExecutor.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY is missing from environment variables.")

    # 1. Initialize Gemini LLM via OpenAI-compatible endpoint
    llm = ChatOpenAI(
        model="gemini-3.5-flash",
        api_key=google_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        temperature=temperature
    )

    # 2. Configure Tools
    search_tool = TavilySearchResults(max_results=max_search_results)
    tools = [search_tool, get_weather_data]

    # 3. Optimized ReAct Prompt with clean direct answering support
    template = (
        "Answer the following questions as best you can. You have access to the following tools:\n\n"
        "{tools}\n\n"
        "Use the following format:\n\n"
        "Question: the input question you must answer\n"
        "Thought: you should always think about what to do\n"
        "Action: the action to take, should be one of [{tool_names}]\n"
        "Action Input: the input to the action\n"
        "Observation: the result of the action\n"
        "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
        "Thought: I now know the final answer\n"
        "Final Answer: the final answer to the original input question\n\n"
        "Important Rule: If you already know the answer directly and do not need to use any tools, "
        "do NOT output Action. Instead, directly write:\n"
        "Thought: I know the answer without needing tools.\n"
        "Final Answer: [your complete answer here]\n\n"
        "Begin!\n\n"
        "Question: {input}\n"
        "Thought:{agent_scratchpad}"
    )
    prompt = PromptTemplate(
        template=template,
        input_variables=["input", "tools", "tool_names", "agent_scratchpad"]
    )

    # 4. Construct Agent & Executor
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        return_intermediate_steps=True
    )

    return agent_executor


if __name__ == "__main__":
    print("Testing Agent from CLI...")
    try:
        executor = get_agent_executor()
        query = "What is the capital of Bangladesh and what is the current weather there?"
        print(f"\nUser Query: {query}\n")
        response = executor.invoke({"input": query})
        print(f"\nFinal Response:\n{response['output']}")
    except Exception as err:
        print(f"Error running agent: {err}")
