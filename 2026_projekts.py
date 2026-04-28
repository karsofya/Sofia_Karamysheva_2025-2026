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
    # LABOJUMS #2 & #3: Dark režīmā vairs netiek ignorētas custom krāsas —
    # tās tiek lietotas vienmēr. Dark režīms tikai maina fonu/tekstu ja nav
    # mainīts manuāli. Fonta izmērs tagad vienmēr ņem vērtību no session state.
    bg = st.session_state.background
    fc = st.session_state.font_color
    fs = st.session_state.font_size
    thc = st.session_state.table_head
    trc = st.session_state.table_row
    bc = st.session_state.table_border

    if st.session_state.theme == "Dark":
        # Tikai ja lietotājs nav mainījis krāsas manuāli, lietojam dark noklusējumus
        if bg == "#ffffff":
            bg = "#0e1117"
        if fc == "#000000":
            fc = "#f0f0f0"
        if trc == "#ffffff":
            trc = "#1a1c23"
        if thc == "#f0f0f0":
            thc = "#1a1c23"
        if bc == "#ddd":
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

        # LABOJUMS #3: Fonta izmēra selectbox tagad izmanto session state vērtību
        # kā sākuma indeksu, nevis vienmēr index=1
        font_options = ["14px", "16px", "18px", "20px"]
        current_font_index = font_options.index(st.session_state.font_size) if st.session_state.font_size in font_options else 1
        st.session_state.font_size = st.selectbox(
            "fonta izmērs",
            font_options,
            index=current_font_index
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
# LABOJUMS #4: Laiks atjaunojas reāllaikā ar JavaScript — bez lapas pārlādēšanas
def header():
    st.title("digitālais panelis")
    st.markdown("""
        <div id="clock" style="font-size:1em; margin-bottom:1rem;"></div>
        <script>
        function updateClock() {
            const now = new Date();
            const hh = String(now.getHours()).padStart(2, '0');
            const mm = String(now.getMinutes()).padStart(2, '0');
            const ss = String(now.getSeconds()).padStart(2, '0');
            const dd = String(now.getDate()).padStart(2, '0');
            const mo = String(now.getMonth() + 1).padStart(2, '0');
            const yyyy = now.getFullYear();
            const el = document.getElementById('clock');
            if (el) el.innerText = hh + ':' + mm + ':' + ss + ' | ' + dd + '.' + mo + '.' + yyyy;
        }
        updateClock();
        setInterval(updateClock, 1000);
        </script>
    """, unsafe_allow_html=True)

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
# LABOJUMS #1: Temperatūra tagad tiek parādīta atsevišķi ar st.metric
# un papildus tekstu, lai nodrošinātu redzamību
def weather_section():
    st.subheader("laikapstākļi")

    try:
        data = weather("Riga,Latvia", st.session_state.force_error)
        cur = data["current_condition"][0]

        temp_c = cur["temp_C"]
        feels_c = cur["FeelsLikeC"]
        desc = cur["weatherDesc"][0]["value"]

        # Rādām temperatūru gan kā metric, gan kā tekstu — lai būtu redzama jebkurā režīmā
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label="Temperatūra",
                value=f"{temp_c} °C",
                delta=f"Sajūta: {feels_c} °C"
            )
        with col2:
            st.markdown(f"**🌡️ {temp_c} °C**")
            st.markdown(f"Sajūta: {feels_c} °C")
            st.markdown(desc)

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