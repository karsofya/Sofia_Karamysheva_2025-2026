# .\venv\Scripts\Activate.ps1
# cd "C:\Users\karso\OneDrive\Documents\Attalinata māciba 2021.2022\Kempelosanas\2026 projekts"; .\venv\Scripts\Activate.ps1; cd Sofia_Karamysheva_2025-2026; streamlit run 2026_projekts.py

# streamlit run "Sofia_Karamysheva_2025-2026\2026_projekts.py"

import streamlit as st
import random
import requests
import pandas as pd
from datetime import date, datetime
import logging
import sys

logging.basicConfig(level=logging.INFO)
logging.info("app start")

# test mode
TESTING_MODE = "--test" in sys.argv

# page config
st.set_page_config(
    page_title="Digitālais informācijas panelis",
    layout="wide"
)

# session state
def init_state():
    defaults = {
        "theme": "Light",
        "notes": "",
        "show_weather": True,
        "show_homework": True,
        "show_notes": True,
        "show_chart": True,
        "debug": False,
        "force_error": False,
        "font_size": "16px",
        "font_color": "#000000",
        "background": "#ffffff",
        "table_head": "#f0f0f0",
        "table_row": "#ffffff",
        "table_border": "#ddd"
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# theme apply
def apply_theme():
    bg = st.session_state.background
    fc = st.session_state.font_color
    fs = st.session_state.font_size
    thc = st.session_state.table_head
    trc = st.session_state.table_row
    bc = st.session_state.table_border

    if st.session_state.theme == "Dark":
        bg = "#0e1117"
        fc = "#f0f0f0"
        trc = "#1a1c23"
        thc = "#1a1c23"
        bc = "#444"

    st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg};
        color: {fc};
        font-size: {fs};
        font-family: Arial;
    }}
    .stMetric {{
        background-color: {trc};
        padding: 10px;
        border-radius: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# sidebar
def sidebar():
    with st.sidebar:
        st.header("iestatījumi")

        st.session_state.theme = st.radio(
            "režīms",
            ["Light", "Dark"],
            index=0 if st.session_state.theme == "Light" else 1
        )

        st.divider()
        st.subheader("sadaļas")

        st.session_state.show_weather = st.checkbox("laikapstākļi", st.session_state.show_weather)
        st.session_state.show_homework = st.checkbox("mājasdarbi", st.session_state.show_homework)
        st.session_state.show_notes = st.checkbox("piezīmes", st.session_state.show_notes)
        st.session_state.show_chart = st.checkbox("grafiks", st.session_state.show_chart)

        st.divider()
        st.subheader("izskats")

        st.session_state.font_size = st.selectbox(
            "fonta izmērs",
            ["14px", "16px", "18px", "20px"],
            index=1
        )

        st.session_state.font_color = st.color_picker("teksts", st.session_state.font_color)
        st.session_state.background = st.color_picker("fons", st.session_state.background)
        st.session_state.table_head = st.color_picker("virsraksts", st.session_state.table_head)
        st.session_state.table_row = st.color_picker("rinda", st.session_state.table_row)
        st.session_state.table_border = st.color_picker("rāmis", st.session_state.table_border)

        if TESTING_MODE:
            st.divider()
            st.subheader("test režīms")

            st.session_state.debug = st.checkbox("debug", st.session_state.debug)

            if st.button("api kļūda"):
                st.session_state.force_error = True

            if st.button("atiestatīt"):
                st.cache_data.clear()
                st.session_state.force_error = False
                st.rerun()

sidebar()
apply_theme()

# header
def header():
    now = datetime.now()
    st.title("digitālais panelis")
    st.markdown(f"{now.strftime('%H:%M:%S')} | {now.strftime('%d.%m.%Y')}")

header()

# weather api
@st.cache_data(ttl=300)
def weather(city, force_error=False):
    if force_error:
        raise Exception("forced error")

    url = f"https://wttr.in/{city}?format=j1"
    r = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})

    if r.status_code != 200:
        raise Exception("api fail")

    return r.json()

# weather ui
def weather_section():
    st.subheader("laikapstākļi")

    try:
        data = weather("Riga,Latvia", st.session_state.force_error)
        cur = data["current_condition"][0]

        st.metric("temperatūra", cur["temp_C"], delta=f"{cur['FeelsLikeC']} sajūta")
        st.write(cur["weatherDesc"][0]["value"])

        if st.session_state.debug:
            st.json(data)

    except Exception as e:
        st.error("kļūda")
        logging.error(e)

        if st.session_state.debug:
            st.exception(e)

# homework ui
def homework_section():
    st.subheader("mājasdarbi")

    data = {
        "priekšmets": ["angļu", "matemātika", "latviešu"],
        "uzdevums": ["eseja", "pd", "eseja"],
        "komentāri": ["rainis", "log", ""],
        "termiņš": [date(2026,1,27), date(2026,1,28), date(2026,1,29)]
    }

    df = pd.DataFrame(data)
    today = date.today()

    df["dienas"] = df["termiņš"].apply(lambda x: (x - today).days)
    df["status"] = df["dienas"].apply(lambda x: "uzmanība" if x <= 2 else "ok")

    st.dataframe(df, use_container_width=True)

# notes ui
def notes_section():
    st.subheader("piezīmes")
    st.session_state.notes = st.text_area("teksts", st.session_state.notes, height=120)

# chart ui
def chart_section():
    st.subheader("grafiks")

    if "chart" not in st.session_state:
        st.session_state.chart = [random.randint(10, 50) for _ in range(20)]

    st.line_chart(pd.DataFrame({"data": st.session_state.chart}))

# card wrapper
def card(title, fn):
    st.markdown(f"### {title}")
    with st.container():
        fn()

# layout
c1, c2 = st.columns(2)

with c1:
    if st.session_state.show_weather:
        card("laikapstākļi", weather_section)
    if st.session_state.show_notes:
        card("piezīmes", notes_section)

with c2:
    if st.session_state.show_homework:
        card("mājasdarbi", homework_section)
    if st.session_state.show_chart:
        card("grafiks", chart_section)

# debug only
if TESTING_MODE and st.session_state.debug:
    st.divider()
    st.json(dict(st.session_state))