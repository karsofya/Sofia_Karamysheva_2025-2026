# .\venv\Scripts\Activate.ps1
# streamlit run 2026_projekts.py

import streamlit as st
import random
import requests
import pandas as pd
import time
from datetime import date, datetime

# ================= PAGE =================
st.set_page_config(
    page_title="Digitālais informācijas panelis",
    layout="wide"
)

# ================= THEME =================
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

with st.sidebar:
    st.header("⚙️ Iestatījumi")

    theme = st.radio(
        "Izvēlies režīmu",
        ["Light", "Dark"],
        index=0 if st.session_state.theme == "Light" else 1
    )
    st.session_state.theme = theme

    if st.button("🔄 Atsvaidzināt paneli"):
        st.cache_data.clear()
        st.rerun()

# Dark mode stils
if st.session_state.theme == "Dark":
    st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# ================= TITLE =================
st.title("📊 Digitālais informācijas panelis")

# ================= CLOCK =================
clock = st.empty()
now = datetime.now()
clock.markdown(
    f"### 🕒 {now.strftime('%H:%M:%S')} | 📅 {now.strftime('%d.%m.%Y')}"
)

# ================= WEATHER =================
@st.cache_data(ttl=300)
def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url, timeout=5)
    return response.json()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🌤️ Laikapstākļi")

    CITY = "Riga"

    try:
        data = get_weather(CITY)
        temp = data["current_condition"][0]["temp_C"]
        feels = data["current_condition"][0]["FeelsLikeC"]
        weather = data["current_condition"][0]["weatherDesc"][0]["value"]

        st.metric("Temperatūra (°C)", temp)
        st.write(f"Sajūta kā: **{feels} °C**")
        st.write(f"Laikapstākļi: **{weather}**")

    except Exception:
        st.error("Nevar iegūt laikapstākļu datus")

# ================= HOMEWORK =================
with col2:
    st.subheader("📚 Mājasdarbi")

    majasdarbi_data = {
        "Priekšmets": ["Angļu valoda", "Matemātika", "Latviešu valoda"],
        "Uzdevums": ["Eseja", "PD", "Eseja"],
        "Komentāri": ["Rainis", "Logaritmi", ""],
        "Termiņš": [
            date(2026, 1, 27),
            date(2026, 1, 28),
            date(2026, 1, 29)
        ]
    }

    df = pd.DataFrame(majasdarbi_data)
    today = date.today()
    df["Dienas palika"] = df["Termiņš"].apply(lambda x: (x - today).days)

    st.table(df)

# ================= NOTES =================
st.subheader("📌 Ātrās piezīmes")

if "notes" not in st.session_state:
    st.session_state.notes = ""

st.session_state.notes = st.text_area(
    "Pieraksti sev svarīgo:",
    st.session_state.notes,
    height=120
)

# ================= CHART =================
st.subheader("📈 Datu grafiks")

chart_data = [random.randint(10, 50) for _ in range(20)]
st.line_chart(chart_data)
