# .\venv\Scripts\Activate.ps1
# cd "C:\Users\karso\OneDrive\Documents\Attalinata māciba 2021.2022\Kempelosanas\2026 projekts"; .\venv\Scripts\Activate.ps1; cd Sofia_Karamysheva_2025-2026; streamlit run 2026_projekts.py

# streamlit run "Sofia_Karamysheva_2025-2026\2026_projekts.py"

import streamlit as st
import random
import requests
import pandas as pd
from datetime import date, datetime

st.set_page_config(
    page_title="Digitālais informācijas panelis",
    layout="wide"
)


def init_session_state():
    defaults = {
        "theme": "Light",
        "notes": "",
        "show_weather": True,
        "show_homework": True,
        "show_notes": True,
        "show_chart": True
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()


def apply_theme():
    if st.session_state.theme == "Dark":
        st.markdown("""
            <style>
            .stApp {
                background-color: #0e1117;
                color: white;
            }
            </style>
        """, unsafe_allow_html=True)

apply_theme()


def render_sidebar():
    with st.sidebar:
        st.header("Iestatījumi")

        st.session_state.theme = st.radio(
            "Izvēlies režīmu",
            ["Light", "Dark"],
            index=0 if st.session_state.theme == "Light" else 1
        )

        st.divider()
        st.subheader("Redzamās sadaļas")

        st.session_state.show_weather = st.checkbox(
            "Laikapstākļi", st.session_state.show_weather
        )
        st.session_state.show_homework = st.checkbox(
            "Mājasdarbi", st.session_state.show_homework
        )
        st.session_state.show_notes = st.checkbox(
            "Piezīmes", st.session_state.show_notes
        )
        st.session_state.show_chart = st.checkbox(
            "Grafiks", st.session_state.show_chart
        )

        st.divider()
        if st.button("Atsvaidzināt paneli"):
            st.cache_data.clear()
            st.rerun()

render_sidebar()


def render_header():
    st.title("Digitālais informācijas panelis")

    now = datetime.now()
    st.markdown(
        f"### {now.strftime('%H:%M:%S')} | {now.strftime('%d.%m.%Y')}"
    )

render_header()


@st.cache_data(ttl=300)
def get_weather(city):
    """
    ONLINE režīms – izmanto wttr.in API
    OFFLINE testam šo funkciju var aizvietot ar fiksētiem datiem
    """
    url = f"https://wttr.in/{city}?format=j1"
    return requests.get(url, timeout=5).json()


def weather_section():
    st.subheader("Laikapstākļi")
    CITY = "Riga"

    try:
        data = get_weather(CITY)
        current = data["current_condition"][0]

        st.metric("Temperatūra (°C)", current["temp_C"])
        st.write(f"Sajūta kā: **{current['FeelsLikeC']} °C**")
        st.write(f"Laikapstākļi: **{current['weatherDesc'][0]['value']}**")

    except Exception:
        st.error("Nevar iegūt laikapstākļu datus")

def homework_section():
    st.subheader("Mājasdarbi")

    data = {
        "Priekšmets": ["Angļu valoda", "Matemātika", "Latviešu valoda"],
        "Uzdevums": ["Eseja", "PD", "Eseja"],
        "Komentāri": ["Rainis", "Logaritmi", ""],
        "Termiņš": [
            date(2026, 1, 27),
            date(2026, 1, 28),
            date(2026, 1, 29)
        ]
    }

    df = pd.DataFrame(data)
    today = date.today()
    df["Dienas palika"] = df["Termiņš"].apply(lambda x: (x - today).days)

    st.dataframe(df, use_container_width=True)

def notes_section():
    st.subheader("Ātrās piezīmes")
    st.session_state.notes = st.text_area(
        "Pieraksti sev svarīgo:",
        st.session_state.notes,
        height=120
    )

def chart_section():
    st.subheader("Datu grafiks")
    data = [random.randint(10, 50) for _ in range(20)]
    st.line_chart(data)

col1, col2 = st.columns(2)

with col1:
    if st.session_state.show_weather:
        weather_section()
    if st.session_state.show_notes:
        notes_section()

with col2:
    if st.session_state.show_homework:
        homework_section()
    if st.session_state.show_chart:
        chart_section()
