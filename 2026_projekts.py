# .\venv\Scripts\Activate.ps1
# cd "C:\Users\karso\OneDrive\Documents\Attalinata māciba 2021.2022\Kempelosanas\2026 projekts"; .\venv\Scripts\Activate.ps1; cd Sofia_Karamysheva_2025-2026; streamlit run 2026_projekts.py

# streamlit run "Sofia_Karamysheva_2025-2026\2026_projekts.py"

import streamlit as st
import random
import requests
import pandas as pd
from datetime import date, datetime
import logging

logging.basicConfig(level=logging.INFO)
logging.info("app started")

# page config
st.set_page_config(
    page_title="Digitālais informācijas panelis",
    layout="wide"
)

# session state
def init_session_state():
    defaults = {
        "theme": "Light",
        "notes": "",
        "show_weather": True,
        "show_homework": True,
        "show_notes": True,
        "show_chart": True,
        "debug_mode": False,
        "force_error": False,
        # customization
        "font_size": "16px",
        "font_color": "#000000",
        "background_color": "#ffffff",
        "table_header_color": "#f0f0f0",
        "table_row_color": "#ffffff",
        "table_border_color": "#ddd"
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# apply theme
def apply_theme():
    bg = st.session_state.background_color
    fc = st.session_state.font_color
    fs = st.session_state.font_size
    thc = st.session_state.table_header_color
    trc = st.session_state.table_row_color
    bc = st.session_state.table_border_color

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
            font-family: 'Arial', sans-serif;
        }}
        .stTextArea, .stDataFrame {{
            background-color: {trc};
            color: {fc};
        }}
        .stDataFrame th {{
            background-color: {thc} !important;
            color: {fc} !important;
        }}
        .stDataFrame td {{
            border: 1px solid {bc} !important;
        }}
        .stMetric {{
            background-color: {trc};
            border-radius: 10px;
            padding: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
        }}
        </style>
    """, unsafe_allow_html=True)

apply_theme()

# sidebar
def render_sidebar(testing=False):  # testing flag
    with st.sidebar:
        st.header("iestatījumi")
        st.session_state.theme = st.radio(
            "izvēlies režīmu",
            ["Light", "Dark"],
            index=0 if st.session_state.theme == "Light" else 1
        )

        st.divider()
        st.subheader("sadaļas")
        st.session_state.show_weather = st.checkbox("laikapstākļi", st.session_state.show_weather)
        st.session_state.show_homework = st.checkbox("mājasdarbi", st.session_state.show_homework)
        st.session_state.show_notes = st.checkbox("piezīmes", st.session_state.show_notes)
        st.session_state.show_chart = st.checkbox("grafiks", st.session_state.show_chart)

        # testing tools only visible to tester
        if testing:
            st.divider()
            st.subheader("testēšana")
            st.session_state.debug_mode = st.checkbox("debug režīms", st.session_state.debug_mode)
            if st.button("simulēt api kļūdu"):
                st.session_state.force_error = True
            if st.button("atsvaidzināt paneli"):
                st.cache_data.clear()
                st.session_state.force_error = False
                st.rerun()

        st.divider()
        st.subheader("izskats")
        st.session_state.font_size = st.selectbox("fonta izmērs", ["14px", "16px", "18px", "20px"], index=1)
        st.session_state.font_color = st.color_picker("teksta krāsa", st.session_state.font_color)
        st.session_state.background_color = st.color_picker("fona krāsa", st.session_state.background_color)
        st.session_state.table_header_color = st.color_picker("tabulas virsraksta krāsa", st.session_state.table_header_color)
        st.session_state.table_row_color = st.color_picker("tabulas rindu krāsa", st.session_state.table_row_color)
        st.session_state.table_border_color = st.color_picker("tabulas rāmja krāsa", st.session_state.table_border_color)

render_sidebar(testing=True)  # change to False for end-user
apply_theme()

# header
def render_header():
    st.title("digitālais informācijas panelis")
    now = datetime.now()
    st.markdown(f"### {now.strftime('%H:%M:%S')} | {now.strftime('%d.%m.%Y')}")

render_header()

# weather
@st.cache_data(ttl=300)
def get_weather(city, force_error=False):
    if force_error:
        raise Exception("simulēta kļūda")
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise Exception("api neatbild")
    return response.json()

def weather_section():
    st.subheader("laikapstākļi")
    CITY = "Riga"
    try:
        data = get_weather(CITY, st.session_state.force_error)
        current = data["current_condition"][0]
        st.metric("temperatūra (°C)", current["temp_C"], delta=f"sajūta: {current['FeelsLikeC']}°C")
        st.write(f"laikapstākļi: **{current['weatherDesc'][0]['value']}**")
        if st.session_state.debug_mode:
            st.write("raw api dati:")
            st.json(data)
    except Exception as e:
        st.error("nevar iegūt laikapstākļu datus")
        logging.error(f"weather error: {e}")
        if st.session_state.debug_mode:
            st.exception(e)

# homework
def homework_section():
    st.subheader("mājasdarbi")
    data = {
        "priekšmets": ["angļu valoda", "matemātika", "latviešu valoda"],
        "uzdevums": ["eseja", "pd", "eseja"],
        "komentāri": ["rainis", "logaritmi", ""],
        "termiņš": [date(2026, 1, 27), date(2026, 1, 28), date(2026, 1, 29)]
    }
    df = pd.DataFrame(data)
    today = date.today()
    df["dienas palika"] = df["termiņš"].apply(lambda x: (x - today).days)
    df["status"] = df["dienas palika"].apply(lambda x: "⚠️" if x <= 2 else "✅")
    st.dataframe(
        df.style.applymap(lambda v: 'background-color: #ffcccc' if v == '⚠️' else '', subset=["status"]),
        use_container_width=True
    )

# notes
def notes_section():
    st.subheader("ātrās piezīmes")
    st.session_state.notes = st.text_area("pieraksti sev svarīgo:", st.session_state.notes, height=120)

# chart
def chart_section():
    st.subheader("datu grafiks")
    data = [random.randint(10, 50) for _ in range(20)]
    st.line_chart(pd.DataFrame({"vērtības": data}), use_container_width=True)

# system
def system_status_section():
    st.subheader("sistēmas statuss")
    st.write("session state:")
    st.json(dict(st.session_state))
    st.write("cache aktīvs (300 sek)")

# card
def section_card(title, content_fn):
    st.markdown(f"<h3 style='margin-bottom:5px'>{title}</h3>", unsafe_allow_html=True)
    st.markdown("<div style='padding:10px; border-radius:10px; background-color:#f7f7f7; box-shadow:2px 2px 5px rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
    content_fn()
    st.markdown("</div>", unsafe_allow_html=True)

# layout
col1, col2 = st.columns(2)

with col1:
    if st.session_state.show_weather:
        section_card("laikapstākļi", weather_section)
    if st.session_state.show_notes:
        section_card("ātrās piezīmes", notes_section)

with col2:
    if st.session_state.show_homework:
        section_card("mājasdarbi", homework_section)
    if st.session_state.show_chart:
        section_card("datu grafiks", chart_section)

# debug for tester only
if st.session_state.debug_mode:
    st.divider()
    system_status_section()