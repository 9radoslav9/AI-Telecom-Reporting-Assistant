import os
import requests
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models

from aggregation import (
    get_revenue_by_region,
    get_new_customers_by_month,
    get_usage_by_plan,
)

load_dotenv()


QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

COLLECTION_NAME = "telecom_aggregates"
EMBEDDING_MODEL_NAME = "intfloat/multilingual-e5-large"
VECTOR_SIZE = 1024

HF_EMBEDDING_URL = f"https://router.huggingface.co/hf-inference/models/{EMBEDDING_MODEL_NAME}/pipeline/feature-extraction"


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)


def embed_text(text: str) -> list[float]:

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"inputs": text}

    response = requests.post(HF_EMBEDDING_URL, headers=headers, json=payload)
    result = response.json()

    return result


def row_to_text(row: dict, source: str) -> str:
    if source == "revenue":
        return f"Регион {row['region']} има общ приход {row['total_revenue']} €."
    elif source == "customers":
        return f"През {row['month']} са регистрирани {row['customer_count']} нови клиента."
    elif source == "usage":
        return (
            f"План {row['plan_name']} има общо {row['total_data_gb']} GB данни, "
            f"{row['total_call_minutes']} минути разговори и {row['total_sms_count']} SMS."
        )
    raise ValueError(f"Непознат source: {source}")


def build_documents() -> list[dict]:
    documents = []

    for row in get_revenue_by_region():
        documents.append({"text": row_to_text(row, "revenue"), "source": "revenue", **row})

    for row in get_new_customers_by_month():
        documents.append({"text": row_to_text(row, "customers"), "source": "customers", **row})

    for row in get_usage_by_plan():
        documents.append({"text": row_to_text(row, "usage"), "source": "usage", **row})

    return documents


def build_vector_index():

    client = get_qdrant_client()
    documents = build_documents()

    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(size=VECTOR_SIZE, distance=models.Distance.COSINE),
    )

    points = []
    for i, doc in enumerate(documents):
        vector = embed_text(doc["text"])
        points.append(models.PointStruct(id=i, vector=vector, payload=doc))

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Индексирани {len(points)} документа в Qdrant Cloud.")


def retrieve_relevant_chunks(question: str, top_k: int = 3) -> list[dict]:
    client = get_qdrant_client()
    question_vector = embed_text(question)

    result = client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_vector,
        limit=top_k,
    )

    return [point.payload for point in result.points]