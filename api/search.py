import os
import openai
import pickle
import numpy as np
import pandas as pd

from typing import List

from tenacity import retry, stop_after_attempt, wait_random_exponential

ORGANIZATION = os.getenv("ORGANIZATION")
API_KEY = os.getenv("API_KEY")

openai.organization = ORGANIZATION
openai.api_key = API_KEY

DATA_PATH = "data/data.csv"
EMBEDDING_CACHE_PATH = "data/embedding_cache.pickle"
ENGINE = "text-similarity-babbage-001"

try:
    EMBEDDING_CACHE = pd.read_pickle(EMBEDDING_CACHE_PATH)
except FileNotFoundError:
    EMBEDDING_CACHE = {}


def read_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.drop_duplicates(subset="id", keep="first")
    df = df.drop_duplicates(subset="name", keep="first")
    df = df.reset_index(drop=True)
    return df


def get_documents(df: pd.DataFrame) -> List:
    documents = []
    for _, query in df.iterrows():
        content = f"{query['name']} {query.description or ''}".strip()
        document = {"id": query.id, "content": content}
        documents.append(document)

    return documents


def _validate_vector(u, dtype=None):
    u = np.asarray(u, dtype=dtype, order='c')
    if u.ndim == 1:
        return u
    raise ValueError("Input vector should be 1-D.")


def _validate_weights(w, dtype=np.double):
    w = _validate_vector(w, dtype=dtype)
    if np.any(w < 0):
        raise ValueError("Input weights should be all non-negative")
    return w


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6))
def get_embedding(text: str, engine="text-similarity-davinci-001") -> List[float]:
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], engine=engine)["data"][0]["embedding"]


def correlation(u, v, w=None, centered=True):
    u = _validate_vector(u)
    v = _validate_vector(v)
    if w is not None:
        w = _validate_weights(w)
    if centered:
        umu = np.average(u, weights=w)
        vmu = np.average(v, weights=w)
        u = u - umu
        v = v - vmu
    uv = np.average(u * v, weights=w)
    uu = np.average(np.square(u), weights=w)
    vv = np.average(np.square(v), weights=w)
    dist = 1.0 - uv / np.sqrt(uu * vv)
    return np.abs(dist)


def cosine(u, v, w=None):
    return max(0, min(correlation(u, v, w=w, centered=False), 2.0))


def distances_from_embeddings(
    query_embedding: List[float],
    embeddings: List[List[float]],
    distance_metric="cosine",
) -> List[List]:
    distance_metrics = {"cosine": cosine}
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding) for embedding in embeddings
    ]
    return distances


def embedding_from_string(string: str, engine: str = ENGINE) -> List:
    if (string, engine) not in EMBEDDING_CACHE.keys():
        EMBEDDING_CACHE[(string, engine)] = get_embedding(string, engine)

    return EMBEDDING_CACHE[(string, engine)]


def find_best_documents(
    query: str,
    documents: List[dict],
    engine: str = ENGINE,
    count: int = 1,
) -> List[int]:
    query_embedding = embedding_from_string(query, engine=engine)
    embeddings = [embedding_from_string(doc["content"], engine=engine) for doc in documents]
    distances = distances_from_embeddings(query_embedding, embeddings, distance_metric="cosine")
    indices_of_nearest_neighbors = np.argsort(distances)

    results = []
    count = min(count, len(documents))
    for idx in indices_of_nearest_neighbors[:count]:
        document = documents[idx]
        results.append(
            {
                "id": document["id"],
                "index": idx,
                "content": document["content"],
                "distance": distances[idx],
            }
        )

    return results


data = read_data(DATA_PATH)
documents = get_documents(data)


def search(query: str) -> dict:
    results = []
    for document in find_best_documents(query, documents, count=3):
        raw_doc = data.iloc[document["index"]]
        results.append(
            {
                "query_id": document["id"],
                "name": raw_doc["name"],
                "distance": document["distance"],
                "sql": raw_doc["query"],
                "visualizations": raw_doc["visualizations"],
            }
        )

    return {"results": results}
