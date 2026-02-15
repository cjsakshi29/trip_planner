import requests
import streamlit as st

OPENWEATHER_API_KEY = st.secrets["OPENWEATHER_API_KEY"]

# ---------------- CURRENT WEATHER ----------------
def get_weather(city):

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]

        return f"Current weather in {city}: {weather}, Temperature: {temp}°C"
    else:
        return "Weather data not available."


# ---------------- WEATHER FORECAST ----------------
def get_forecast(city):

    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    forecast_text = "5-Day Forecast:\n"

    if response.status_code == 200:
        for i in range(0, 5):
            forecast = data["list"][i]
            date = forecast["dt_txt"]
            temp = forecast["main"]["temp"]
            condition = forecast["weather"][0]["description"]

            forecast_text += f"{date} - {condition}, {temp}°C\n"

        return forecast_text

    else:
        return "Forecast data not available."


# ---------------- FLIGHT TOOL ----------------
def get_flights(city):

    return f"""
Flight Options to {city}:
- Air India AI302 – Direct – ₹45,000
- Emirates EK319 – 1 Stop – ₹52,000
- ANA NH123 – Direct – ₹48,500
"""


# ---------------- HOTEL TOOL ----------------
def get_hotels(city):

    return f"""
Hotel Options in {city}:
- Park Hotel – 4⭐ – ₹9,500/night
- City Central Hotel – 3⭐ – ₹6,500/night
- Budget Stay Inn – ₹3,000/night
"""
