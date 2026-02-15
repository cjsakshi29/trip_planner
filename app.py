import streamlit as st
import os
import requests
from dotenv import load_dotenv
from langchain.tools import Tool

from tools import get_weather, get_forecast, get_flights, get_hotels

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ----------- PAGE CONFIG -----------
st.set_page_config(page_title="AI Trip Planner", layout="wide")

st.title("🌍 AI Trip Planner Agent")

prompt = st.text_input("Enter your trip request")

if st.button("Plan Trip"):

    if prompt:

        with st.spinner("Generating trip plan..."):

            # Extract city
            try:
                city = prompt.split("to")[1].split("in")[0].strip()
            except:
                city = prompt

            # Call tools
            weather = get_weather(city)
            forecast = get_forecast(city)
            flights = get_flights(city)
            hotels = get_hotels(city)

            # Combine tool outputs
            combined_data = f"""
            {weather}

            {forecast}

            {flights}

            {hotels}
            """

            # Call OpenRouter LLM directly
            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "Trip Planner"
            }

            final_prompt = f"""
            {prompt}

            Here is real-time data:

            {combined_data}

            Using this data:
            - Write one paragraph about cultural significance.
            - Suggest travel dates.
            - Include the above weather.
            - Include forecast during trip.
            - Include flight options.
            - Include hotel options.
            - Provide day-wise itinerary.
            """

            data = {
                "model": "meta-llama/llama-3-8b-instruct",
                "messages": [
                    {"role": "user", "content": final_prompt}
                ]
            }

            response = requests.post(url, headers=headers, json=data)
            result = response.json()

            if response.status_code == 200:
                trip_text = result["choices"][0]["message"]["content"]
            else:
                trip_text = "Error generating response."

        st.markdown(trip_text)

    else:
        st.warning("Please enter a prompt.")
