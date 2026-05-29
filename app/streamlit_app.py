import streamlit as st

st.set_page_config(
    page_title="Interview simulator",
    page_icon="🎙️",
    layout="centered",
)

st.title("Interview simulator")

st.write(
    "Тренажер технических собеседований. "
    "Выбери направление, уровень и формат интервью."
)

track = st.selectbox(
    "Направление", 
    ["Python", "Backend", "Machine Learning", "Data Engineering"],
)

level = st.selectbox(
    "Grade", 
    ["junoir", "middle", "senior"]
)

mode = st.radio(
    "Формат интервью",
    ["Theory", "Practice", "Mixed"],
)

if st.button("Начать интервью"):
    st.success("Интервью создано")
    st.write(f"Направление: {track}")
    st.write(f"Уровень: {level}")
    st.write(f"Формат: {mode}")