import streamlit as st
import pandas as pd
from pipeline import run_pipeline
from rag import build_vector_index
from agent import run_agent


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

st.divider()
st.subheader("Свободен въпрос")

if st.button("Обнови RAG индекса"):
    with st.spinner("Индексирам данните в Qdrant..."):
        build_vector_index()
    st.success("Индексът е обновен.")

question = st.text_input("Задай въпрос за данните (свободен текст):")

if st.button("Питай") and question:
    with st.spinner("Анализирам въпроса и генерирам отговор..."):
        result = run_agent(question)

    route = result["route"]
    label_map = {"revenue": "region", "customers": "month", "usage": "plan_name"}

    if route == "general":
        st.write("**Отговор:**", result["rag_answer"])
        with st.expander("Кои данни бяха използвани?"):
            for chunk in result["rag_chunks"]:
                st.write("-", chunk["text"])
    else:
        st.caption(f"Разпознат като фиксиран въпрос: {route}")
        show_result(result["pipeline_result"], label_map[route])