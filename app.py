import streamlit as st
import pandas as pd
from pipeline import run_pipeline
from rag import build_vector_index, retrieve_relevant_chunks
from LLM import generate_rag_answer


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
st.subheader("Свободен въпрос (RAG)")

if st.button("Обнови RAG индекса"):
    with st.spinner("Индексирам данните в Qdrant..."):
        build_vector_index()
    st.success("Индексът е обновен.")

question = st.text_input("Задай въпрос за данните:")

if st.button("Питай") and question:
    with st.spinner("Търся релевантни данни и генерирам отговор..."):
        chunks = retrieve_relevant_chunks(question, top_k=3)
        answer = generate_rag_answer(question, chunks)

    st.write("**Отговор:**", answer)

    with st.expander("Кои данни бяха използвани?"):
        for chunk in chunks:
            st.write("-", chunk["text"])
