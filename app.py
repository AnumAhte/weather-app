import streamlit as st
import requests
import os
import pandas as pd
from dotenv import load_dotenv
from io import StringIO

# 🔐 Load API Key from .env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# 🔽 Hide Streamlit Menu, Header, and Footer
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}  /* Hide Streamlit menu */
        header {visibility: hidden;}  /* Hide header */
        footer {visibility: hidden;}  /* Hide footer */
    </style>
    """,
    unsafe_allow_html=True
)

# 🎨 Modern Theme (Glassmorphism)
st.markdown(
    """
    <style>
        body { background-color: #121212; color: white; font-family: 'Poppins', sans-serif; }
        .stApp { background: linear-gradient(135deg, #1f4037 10%, #99f2c8 100%); padding: 20px; border-radius: 15px; }
        .stTextInput>div>div>input { background-color: rgba(255, 255, 255, 0.2); color: black; border-radius: 8px; padding: 12px; font-size: 16px; }
        .stButton>button { background: linear-gradient(135deg, #12c2e9, #c471ed, #f64f59); color: white; border-radius: 10px; padding: 12px 20px; font-size: 18px; font-weight: bold; border: none; }
        .stButton>button:hover { background: linear-gradient(135deg, #f64f59, #c471ed, #12c2e9); }
        .weather-box { background: rgba(255, 255, 255, 0.2); padding: 20px; border-radius: 12px; text-align: center; color: white; }
        .weather-box h2 { font-size: 28px; margin-bottom: 10px; }
        .weather-box h3 { font-size: 22px; margin-bottom: 5px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# 🏡 App Title
st.markdown("<h1 style='text-align: center;'>🌦️ Real-Time Weather App</h1>", unsafe_allow_html=True)

# 🌍 User Input for City
city = st.text_input("Enter City Name", placeholder="E.g., Lahore, Karachi, New York")

# 🔍 Get Weather Button
if st.button("Get Weather"):
    if city:
        if API_KEY:
            try:
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                response = requests.get(url)
                data = response.json()

                if response.status_code == 200:
                    weather = data['weather'][0]['description'].title()
                    temp = data['main']['temp']
                    humidity = data['main']['humidity']
                    wind_speed = data['wind']['speed']
                    country = data['sys']['country']
                    weather_icon = data['weather'][0]['icon']

                    # 🌞 Weather Display with Icon
                    st.markdown(f"""
                        <div class="weather-box">
                            <img src="http://openweathermap.org/img/wn/{weather_icon}@2x.png" width="100">
                            <h2>📍 {city.title()}, {country}</h2>
                            <h3>🌡️ {temp}°C</h3>
                            <h3>🌤️ {weather}</h3>
                            <h3>💧 Humidity: {humidity}%</h3>
                            <h3>🌬️ Wind Speed: {wind_speed} m/s</h3>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # 📂 Download Options
                    weather_data = pd.DataFrame({
                        "City": [city.title()],
                        "Country": [country],
                        "Temperature (°C)": [temp],
                        "Weather": [weather],
                        "Humidity (%)": [humidity],
                        "Wind Speed (m/s)": [wind_speed]
                    })
                    
                    csv = weather_data.to_csv(index=False)
                    txt = weather_data.to_string(index=False)
                    
                    st.download_button(
                        "📥 Download as CSV", data=csv, file_name="weather_report.csv", mime="text/csv"
                    )
                    
                    st.download_button(
                        "📥 Download as TXT", data=txt, file_name="weather_report.txt", mime="text/plain"
                    )
                else:
                    st.error("⚠️ City not found! Please try again.")

            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.error("❌ API Key is missing! Please set it in your .env file.")
    else:
        st.warning("⚠️ Please enter a city name.")
