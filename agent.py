from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from pipeline import run_pipeline
from rag import retrieve_relevant_chunks
from LLM_langchain import classify_question, generate_rag_answer_langchain


class AgentState(TypedDict):
    question: str
    route: str
    pipeline_result: dict
    rag_answer: str
    rag_chunks: list


def classify_node(state: AgentState) -> dict:
    route = classify_question(state["question"])
    return {"route": route}


def fixed_node(state: AgentState) -> dict:
    result = run_pipeline(state["route"])
    return {"pipeline_result": result}


def rag_node(state: AgentState) -> dict:
    chunks = retrieve_relevant_chunks(state["question"], top_k=3)
    answer = generate_rag_answer_langchain(state["question"], chunks)
    return {"rag_chunks": chunks, "rag_answer": answer}


def route_by_classification(state: AgentState) -> str:
    return state["route"]


builder = StateGraph(AgentState)

builder.add_node("classify", classify_node)
builder.add_node("fixed", fixed_node)
builder.add_node("rag", rag_node)

builder.add_edge(START, "classify")
builder.add_conditional_edges(
    "classify",
    route_by_classification,
    {
        "revenue": "fixed",
        "customers": "fixed",
        "usage": "fixed",
        "general": "rag",
    },
)
builder.add_edge("fixed", END)
builder.add_edge("rag", END)

graph = builder.compile()


def run_agent(question: str) -> dict:
    return graph.invoke({"question": question})