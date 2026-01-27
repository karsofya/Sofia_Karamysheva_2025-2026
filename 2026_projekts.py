##.\venv\Scripts\Activate.ps1
#streamlit run 2026_projekts.py
import streamlit as st
import random
import requests
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Digitālais informācijas panelis",
    layout="wide"
)

st.title("📊\ Digitālais informācijas panelis")

# ================= WEATHER =================
@st.cache_data(ttl=300)  # atjauno ik pēc 5 min
def get_weather(city):
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url, timeout=5)
    return response.json()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Laikapstākļi")

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

with col2:
    majasdarbi_data = {
        "Priekšmets": ["Angļu valoda", "Matemātika", "Latviešu valoda"],
        "Uzdevums": [":blue[Eseja]", ":green[PD]", ":blue[Eseja]"],
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

    st.table(df, border="horizontal")



# ================= CHART =================
st.subheader(" Datu grafiks")

chart_data = [random.randint(10, 50) for _ in range(20)]
st.line_chart(chart_data)