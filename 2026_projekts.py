# .\venv\Scripts\Activate.ps1
# cd "C:\Users\karso\OneDrive\Documents\Attalinata māciba 2021.2022\Kempelosanas\2026 projekts"; .\venv\Scripts\Activate.ps1; cd Sofia_Karamysheva_2025-2026; streamlit run 2026_projekts.py
# streamlit run "Sofia_Karamysheva_2025-2026\2026_projekts.py"

import streamlit as st
import random
import requests
import pandas as pd
from datetime import date
import logging
import sys

logging.basicConfig(level=logging.INFO)
logging.info("app start")

TESTING_MODE = "--test" in sys.argv

st.set_page_config(
    page_title="Digitālais informācijas panelis",
    layout="wide"
)

# ── Session state ────────────────────────────────────────────────────────────

def init_state():
    defaults = {
        "theme": "Light",
        "notes": "",
        "show_weather": True,
        "show_homework": True,
        "show_notes": True,
        "show_chart": True,
        "show_joke": True,
        "show_fact": True,
        "show_currency": True,
        "debug": False,
        "force_error": False,
        "font_size": "16px",
        "font_color": "#000000",
        "background": "#ffffff",
        "table_head": "#f0f0f0",
        "table_row": "#ffffff",
        "table_border": "#dddddd",
        "homework_data": None,
        "joke_text": None,
        "fact_text": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Theme ────────────────────────────────────────────────────────────────────

def apply_theme():
    bg  = st.session_state.background
    fc  = st.session_state.font_color
    fs  = st.session_state.font_size
    thc = st.session_state.table_head
    trc = st.session_state.table_row
    bc  = st.session_state.table_border

    is_dark = st.session_state.theme == "Dark"

    if is_dark:
        if bg  == "#ffffff":  bg  = "#0e1117"
        if fc  == "#000000":  fc  = "#f0f0f0"
        if trc == "#ffffff":  trc = "#1a1c23"
        if thc == "#f0f0f0":  thc = "#262730"
        if bc  == "#dddddd":  bc  = "#444444"

    sidebar_bg = "#1a1c23" if is_dark else "#f5f5f5"
    input_bg   = "#262730" if is_dark else "#ffffff"
    btn_bg     = "#3a3d4a" if is_dark else "#f0f2f6"
    btn_hover  = "#4a4d5e" if is_dark else "#e0e2ea"

    # Glide Data Grid colour tokens
    if is_dark:
        gdg_bg        = "#1a1c23"
        gdg_header_bg = "#262730"
        gdg_text      = "#f0f0f0"
        gdg_border    = "#444444"
        gdg_selection = "#3a3d4a"
        gdg_accent    = "#4a90d9"
    else:
        gdg_bg        = "#ffffff"
        gdg_header_bg = "#f0f0f0"
        gdg_text      = "#000000"
        gdg_border    = "#dddddd"
        gdg_selection = "#e8f0fe"
        gdg_accent    = "#4a90d9"

    st.markdown(f"""
    <style>
    /* ── Main app background & text ── */
    .stApp {{
        background-color: {bg} !important;
        color: {fc} !important;
        font-size: {fs};
        font-family: Arial;
    }}
    .stApp p, .stApp li, .stApp label, .stApp span,
    .stApp h1, .stApp h2, .stApp h3, .stApp div {{
        color: {fc} !important;
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
    }}
    [data-testid="stSidebar"] * {{
        color: {fc} !important;
    }}

    /* ── Buttons ── */
    .stButton > button {{
        background-color: {btn_bg} !important;
        color: {fc} !important;
        border: 1px solid {bc} !important;
        border-radius: 6px;
    }}
    .stButton > button:hover {{
        background-color: {btn_hover} !important;
        color: {fc} !important;
    }}

    /* ── Text area (Piezīmes) ── */
    .stTextArea textarea {{
        background-color: {input_bg} !important;
        color: {fc} !important;
        border: 1px solid {bc} !important;
    }}

    /* ── Selectbox / radio in sidebar ── */
    .stSelectbox div[data-baseweb="select"] > div,
    .stRadio div[role="radiogroup"] label {{
        background-color: {input_bg} !important;
        color: {fc} !important;
    }}

    /* ══════════════════════════════════════════════════════
       DATA EDITOR
       The grid is painted on <canvas> via Glide Data Grid,
       so th/td selectors have zero effect. We use two
       approaches together:
         1. CSS custom properties on the wrapper + children
         2. A JS MutationObserver that sets them at runtime
            directly on the DOM nodes GDG actually reads.
    ══════════════════════════════════════════════════════ */
    [data-testid="stDataEditor"],
    [data-testid="stDataEditor"] * {{
        --gdg-bg-cell:                {gdg_bg} !important;
        --gdg-bg-cell-medium:         {gdg_bg} !important;
        --gdg-bg-header:              {gdg_header_bg} !important;
        --gdg-bg-header-has-focus:    {gdg_header_bg} !important;
        --gdg-bg-header-hovered:      {gdg_selection} !important;
        --gdg-text-dark:              {gdg_text} !important;
        --gdg-text-medium:            {gdg_text} !important;
        --gdg-text-light:             {gdg_text} !important;
        --gdg-text-header:            {gdg_text} !important;
        --gdg-border-color:           {gdg_border} !important;
        --gdg-horizontal-border-color:{gdg_border} !important;
        --gdg-accent-color:           {gdg_accent} !important;
        --gdg-bg-search-result:       {gdg_selection} !important;
        --gdg-link-color:             {gdg_accent} !important;
    }}

    /* Stretch the table to full card width, no inner scrollbar */
    [data-testid="stDataEditor"] {{
        width: 100% !important;
        min-width: 0 !important;
    }}
    [data-testid="stDataEditor"] > div,
    [data-testid="stDataEditor"] > div > div {{
        width: 100% !important;
        overflow: visible !important;
        background-color: {gdg_bg} !important;
    }}
    [data-testid="stDataEditor"] canvas {{
        background-color: {gdg_bg} !important;
    }}

    /* Cell-edit overlay popup */
    .glide-data-grid-portal,
    .glide-data-grid-portal * {{
        --gdg-bg-cell:   {gdg_bg} !important;
        --gdg-text-dark: {gdg_text} !important;
        background-color: {input_bg} !important;
        color: {fc} !important;
        border-color: {bc} !important;
    }}
    .glide-data-grid-portal input,
    .glide-data-grid-portal textarea {{
        background-color: {input_bg} !important;
        color: {fc} !important;
        border: 1px solid {bc} !important;
    }}

    /* ── Line chart ── */
    [data-testid="stArrowVegaLiteChart"] {{
        background-color: {input_bg} !important;
        border-radius: 8px;
        padding: 8px;
    }}

    /* ── Metric cards ── */
    .stMetric {{
        background-color: {trc} !important;
        padding: 10px;
        border-radius: 10px;
    }}
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"] {{
        color: {fc} !important;
    }}

    /* ── Info / success / warning / error alert boxes ── */
    [data-testid="stAlert"] {{
        background-color: {input_bg} !important;
    }}
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] div,
    [data-testid="stAlert"] span {{
        color: {fc} !important;
    }}

    /* ── Containers / cards ── */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: {trc} !important;
        border-color: {bc} !important;
    }}

    /* ── Card title bar ── */
    .dash-title {{
        background-color: {thc} !important;
        color: {fc} !important;
        border-radius: 8px 8px 0 0;
        padding: 6px 12px;
        margin: -4px -16px 10px -16px;
        font-size: 1.15em;
        font-weight: bold;
    }}

    /* ── Caption text ── */
    .stCaption, [data-testid="stCaptionContainer"] {{
        color: {fc} !important;
        opacity: 0.8;
    }}

    /* ── Checkbox labels in sidebar ── */
    [data-testid="stCheckbox"] label span {{
        color: {fc} !important;
    }}

    /* ── Color picker labels ── */
    [data-testid="stColorPicker"] label {{
        color: {fc} !important;
    }}
    </style>

    <script>
    /* ── JS runtime patch for Glide Data Grid ──────────────────────────
       GDG reads CSS variables from the element it renders into, but
       Streamlit re-mounts the component after every rerun, wiping any
       previous inline styles. A MutationObserver re-applies the vars
       every time GDG's DOM nodes appear or change.
    ─────────────────────────────────────────────────────────────────── */
    (function() {{
        const VARS = {{
            '--gdg-bg-cell':                 '{gdg_bg}',
            '--gdg-bg-cell-medium':          '{gdg_bg}',
            '--gdg-bg-header':               '{gdg_header_bg}',
            '--gdg-bg-header-has-focus':     '{gdg_header_bg}',
            '--gdg-bg-header-hovered':       '{gdg_selection}',
            '--gdg-text-dark':               '{gdg_text}',
            '--gdg-text-medium':             '{gdg_text}',
            '--gdg-text-light':              '{gdg_text}',
            '--gdg-text-header':             '{gdg_text}',
            '--gdg-border-color':            '{gdg_border}',
            '--gdg-horizontal-border-color': '{gdg_border}',
            '--gdg-accent-color':            '{gdg_accent}',
            '--gdg-bg-search-result':        '{gdg_selection}',
        }};

        function applyToEl(el) {{
            Object.entries(VARS).forEach(([k, v]) => el.style.setProperty(k, v, 'important'));
            el.style.setProperty('background-color', '{gdg_bg}', 'important');
        }}

        function patch() {{
            /* Top-level wrapper */
            document.querySelectorAll('[data-testid="stDataEditor"]').forEach(applyToEl);
            /* Inner GDG stack / canvas wrapper */
            document.querySelectorAll('.dvn-stack, .gdg-style').forEach(applyToEl);
            /* The canvas itself */
            document.querySelectorAll('[data-testid="stDataEditor"] canvas').forEach(c => {{
                c.style.setProperty('background-color', '{gdg_bg}', 'important');
            }});
        }}

        patch();
        if (!window.__gdgObserver) {{
            window.__gdgObserver = new MutationObserver(patch);
            window.__gdgObserver.observe(document.body, {{ childList: true, subtree: true }});
        }}
    }})();
    </script>
    """, unsafe_allow_html=True)

apply_theme()

# ── Sidebar ──────────────────────────────────────────────────────────────────

def sidebar():
    with st.sidebar:
        st.header("Iestatījumi")

        st.session_state.theme = st.radio(
            "Režīms",
            ["Light", "Dark"],
            index=0 if st.session_state.theme == "Light" else 1
        )

        st.divider()
        st.subheader("Sadaļas")
        st.session_state.show_weather  = st.checkbox("Laikapstākļi",     st.session_state.show_weather)
        st.session_state.show_homework = st.checkbox("Mājasdarbi",        st.session_state.show_homework)
        st.session_state.show_notes    = st.checkbox("Piezīmes",          st.session_state.show_notes)
        st.session_state.show_chart    = st.checkbox("Grafiks",           st.session_state.show_chart)
        st.session_state.show_joke     = st.checkbox("Joks",              st.session_state.show_joke)
        st.session_state.show_fact     = st.checkbox("Interesants fakts", st.session_state.show_fact)
        st.session_state.show_currency = st.checkbox("Valūtas kurss",     st.session_state.show_currency)

        st.divider()
        st.subheader("Izskats")

        font_options = ["14px", "16px", "18px", "20px"]
        fi = font_options.index(st.session_state.font_size) if st.session_state.font_size in font_options else 1
        st.session_state.font_size    = st.selectbox("Fonta izmērs", font_options, index=fi)
        st.session_state.font_color   = st.color_picker("Teksts",     st.session_state.font_color)
        st.session_state.background   = st.color_picker("Fons",       st.session_state.background)
        st.session_state.table_head   = st.color_picker("Virsraksts", st.session_state.table_head)
        st.session_state.table_row    = st.color_picker("Rinda",      st.session_state.table_row)
        st.session_state.table_border = st.color_picker("Rāmis",      st.session_state.table_border)

        if TESTING_MODE:
            st.divider()
            st.subheader("Test režīms")
            st.session_state.debug = st.checkbox("Debug", st.session_state.debug)
            if st.button("Api kļūda"):
                st.session_state.force_error = True
            if st.button("Atiestatīt"):
                st.cache_data.clear()
                st.session_state.force_error = False
                st.rerun()

sidebar()
apply_theme()  # re-apply after sidebar widget changes

# ── Header ───────────────────────────────────────────────────────────────────

def header():
    st.title("Digitālais panelis")
    st.markdown("""
        <div id="clock" style="font-size:1em; margin-bottom:1rem;"></div>
        <script>
        function updateClock() {
            const now = new Date();
            const hh = String(now.getHours()).padStart(2,'0');
            const mm = String(now.getMinutes()).padStart(2,'0');
            const ss = String(now.getSeconds()).padStart(2,'0');
            const dd = String(now.getDate()).padStart(2,'0');
            const mo = String(now.getMonth()+1).padStart(2,'0');
            const yyyy = now.getFullYear();
            const el = document.getElementById('clock');
            if (el) el.innerText = hh+':'+mm+':'+ss+' | '+dd+'.'+mo+'.'+yyyy;
        }
        updateClock();
        setInterval(updateClock, 1000);
        </script>
    """, unsafe_allow_html=True)

header()

# ── API fetchers ─────────────────────────────────────────────────────────────

@st.cache_data(ttl=300)
def fetch_weather(city, force_error=False):
    if force_error:
        raise Exception("Forced error")
    r = requests.get(
        f"https://wttr.in/{city}?format=j1",
        timeout=5,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    if r.status_code != 200:
        raise Exception("API fail")
    return r.json()

@st.cache_data(ttl=3600)
def fetch_joke():
    r = requests.get(
        "https://icanhazdadjoke.com/",
        headers={"Accept": "application/json"},
        timeout=5
    )
    r.raise_for_status()
    return r.json()["joke"]

@st.cache_data(ttl=3600)
def fetch_fact():
    r = requests.get(
        "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en",
        timeout=5
    )
    r.raise_for_status()
    return r.json()["text"]

@st.cache_data(ttl=600)
def fetch_currency():
    r = requests.get(
        "https://api.frankfurter.app/latest?from=EUR&to=USD,GBP,SEK,PLN",
        timeout=5
    )
    r.raise_for_status()
    return r.json()

# ── Section renderers ─────────────────────────────────────────────────────────

def weather_section():
    try:
        data    = fetch_weather("Riga,Latvia", st.session_state.get("force_error", False))
        cur     = data["current_condition"][0]
        temp_c  = cur["temp_C"]
        feels_c = cur["FeelsLikeC"]
        desc    = cur["weatherDesc"][0]["value"]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Temperatūra", f"{temp_c} °C", f"Sajūta: {feels_c} °C")
        with col2:
            st.markdown(f"**🌡️ {temp_c} °C**")
            st.markdown(f"Sajūta: {feels_c} °C")
            st.markdown(desc)

        if st.session_state.debug:
            st.json(data)
    except Exception as e:
        st.error("Kļūda ielādējot laikapstākļus")
        logging.error(e)
        if st.session_state.debug:
            st.exception(e)


def homework_section():
    if st.session_state.homework_data is None:
        st.session_state.homework_data = pd.DataFrame({
            "Priekšmets": ["Angļu",   "Matemātika", "Latviešu"],
            "Uzdevums":   ["Eseja",   "Pd",          "Eseja"],
            "Komentāri":  ["Rainis",  "Log",         ""],
            "Termiņš":    [date(2026, 1, 27), date(2026, 1, 28), date(2026, 1, 29)],
        })

    today = date.today()

    # Dynamic height: all rows visible, no inner scrollbar
    row_count = len(st.session_state.homework_data)
    table_height = (row_count + 1) * 35 + 40

    edited = st.data_editor(
        st.session_state.homework_data,
        num_rows="dynamic",
        use_container_width=True,
        height=table_height,
        column_config={
            "Termiņš": st.column_config.DateColumn("Termiņš", format="DD.MM.YYYY"),
        },
        key="homework_editor"
    )
    st.session_state.homework_data = edited

    if not edited.empty and "Termiņš" in edited.columns:
        def days_left(d):
            try:
                return (d - today).days
            except Exception:
                return None
        days_col = edited["Termiņš"].apply(days_left)
        urgent_count = days_col.apply(lambda x: x is not None and x <= 2).sum()
        if urgent_count:
            st.warning(f"⚠️ {urgent_count} uzdevum(i) ar termiņu 2 dienās vai mazāk!")


def notes_section():
    st.session_state.notes = st.text_area(
        "Teksts", st.session_state.notes, height=120, label_visibility="collapsed"
    )


def chart_section():
    if "chart" not in st.session_state:
        st.session_state.chart = [random.randint(10, 50) for _ in range(20)]
    _, btn_col = st.columns([4, 1])
    with btn_col:
        if st.button("🔄 Atjaunot"):
            st.session_state.chart = [random.randint(10, 50) for _ in range(20)]
    st.line_chart(pd.DataFrame({"Dati": st.session_state.chart}))


def joke_section():
    try:
        if st.session_state.joke_text is None:
            st.session_state.joke_text = fetch_joke()
        st.info(f"😄 {st.session_state.joke_text}")
        if st.button("Jauns joks 🎲"):
            fetch_joke.clear()
            st.session_state.joke_text = None
            st.rerun()
    except Exception as e:
        st.error("Kļūda ielādējot joku")
        logging.error(e)


def fact_section():
    try:
        if st.session_state.fact_text is None:
            st.session_state.fact_text = fetch_fact()
        st.success(f"💡 {st.session_state.fact_text}")
        if st.button("Jauns fakts 🎲"):
            fetch_fact.clear()
            st.session_state.fact_text = None
            st.rerun()
    except Exception as e:
        st.error("Kļūda ielādējot faktu")
        logging.error(e)


def currency_section():
    try:
        data     = fetch_currency()
        base     = data["base"]
        rates    = data["rates"]
        date_str = data.get("date", "")

        st.caption(f"Bāze: {base} · Datums: {date_str}")
        flags = {"USD": "🇺🇸", "GBP": "🇬🇧", "SEK": "🇸🇪", "PLN": "🇵🇱"}
        cols  = st.columns(len(rates))
        for col, (currency, rate) in zip(cols, rates.items()):
            with col:
                st.metric(
                    label=f"{flags.get(currency, '')} {currency}",
                    value=f"{rate:.4f}"
                )
    except Exception as e:
        st.error("Kļūda ielādējot valūtas kursu")
        logging.error(e)

# ── Card wrapper ──────────────────────────────────────────────────────────────

def card(title, fn):
    with st.container(border=True):
        st.markdown(
            f'<div class="dash-title">{title}</div>',
            unsafe_allow_html=True
        )
        fn()

# ── Layout ────────────────────────────────────────────────────────────────────

c1, c2 = st.columns(2)

with c1:
    if st.session_state.show_weather:
        card("🌤️ Laikapstākļi", weather_section)
    if st.session_state.show_notes:
        card("📝 Piezīmes", notes_section)
    if st.session_state.show_joke:
        card("😄 Joks", joke_section)

with c2:
    if st.session_state.show_homework:
        card("📚 Mājasdarbi", homework_section)
    if st.session_state.show_chart:
        card("📈 Grafiks", chart_section)
    if st.session_state.show_fact:
        card("💡 Interesants fakts", fact_section)

if st.session_state.show_currency:
    card("💱 Valūtas kurss (EUR)", currency_section)

# ── Debug panel ───────────────────────────────────────────────────────────────

if TESTING_MODE and st.session_state.debug:
    st.divider()
    st.json(dict(st.session_state))