import streamlit as st
import os
from dotenv import load_dotenv
import requests
import base64

from langchain_core.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI

from tools import get_weather, get_forecast, get_flights, get_hotels

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ---------------- LLM SETUP ----------------
llm = ChatOpenAI(
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    model_name="meta-llama/llama-3-8b-instruct",
    temperature=0.7
)

# ---------------- DEFINE TOOLS ----------------
tools = [
    Tool(name="Current Weather", func=get_weather, description="Get current weather"),
    Tool(name="Weather Forecast", func=get_forecast, description="Get 5-day forecast"),
    Tool(name="Flight Options", func=get_flights, description="Get flight details"),
    Tool(name="Hotel Options", func=get_hotels, description="Get hotel details"),
]

agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False)

# ---------------- STREAMLIT UI ----------------
st.set_page_config(page_title="AI Trip Planner", layout="wide")

st.title("🌍 AI Trip Planner Agent (LangChain Powered)")

prompt = st.text_input("Enter your trip request")

if st.button("Plan Trip"):

    if prompt:

        with st.spinner("Generating trip plan..."):

            result = agent.run(
                f"""
                {prompt}

                Provide:
                1 paragraph about city's cultural & historical significance.
                Include current weather.
                Include forecast during travel.
                Include flight options.
                Include hotel options.
                Include day-wise itinerary.
                """
            )

        st.markdown(result)

    else:
        st.warning("Please enter a trip request.")
