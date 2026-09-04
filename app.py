import streamlit as st
import pandas as pd
from pipeline import run_pipeline


def show_result(result, label_field):
    st.subheader("Сурови данни")
    st.dataframe(result["data"])

    st.subheader("LLM резюме")
    st.write(result["summary"])

    st.subheader("Проверка на числата")
    verification_rows = []
    for row, field, status in result["verification"]:
        icon = "✅" if status == "намерено" else "⚠️"
        verification_rows.append({
            "ред": row[label_field],
            "поле": field,
            "стойност": row[field],
            "статус": f"{icon} {status}"
        })
    st.dataframe(pd.DataFrame(verification_rows))


st.title("AI Telecom Reporting Assistant")

st.sidebar.header("Избери въпрос")
question = st.sidebar.radio(
    "Кой отчет искаш да видиш?",
    ["Revenue by region", "New customers by month", "Usage by plan"]
)

question_map = {
    "Revenue by region": ("revenue", "region"),
    "New customers by month": ("customers", "month"),
    "Usage by plan": ("usage", "plan_name"),
}

if st.sidebar.button("Генерирай"):
    pipeline_key, label_field = question_map[question]
    with st.spinner("Генерирам резюме..."):
        result = run_pipeline(pipeline_key)
    show_result(result, label_field)