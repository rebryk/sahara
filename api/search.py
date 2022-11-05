import os
import openai
import pickle
import pandas as pd

from typing import List
from openai import embeddings_utils as utils

ORGANIZATION = os.getenv("ORGANIZATION")
API_KEY = os.getenv("API_KEY")

openai.organization = ORGANIZATION
openai.api_key = API_KEY

DATA_PATH = "data.csv"
EMBEDDING_CACHE_PATH = "embedding_cache.pickle"
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


def embedding_from_string(string: str, engine: str = ENGINE) -> List:
    if (string, engine) not in EMBEDDING_CACHE.keys():
        EMBEDDING_CACHE[(string, engine)] = utils.get_embedding(string, engine)

        with open(EMBEDDING_CACHE_PATH, "wb") as embedding_cache_file:
            pickle.dump(EMBEDDING_CACHE, embedding_cache_file)

    return EMBEDDING_CACHE[(string, engine)]


def find_best_documents(
    query: str,
    documents: List[dict],
    engine: str = ENGINE,
    count: int = 1,
) -> List[int]:
    query_embedding = embedding_from_string(query, engine=engine)
    embeddings = [embedding_from_string(doc["content"], engine=engine) for doc in documents]
    distances = utils.distances_from_embeddings(
        query_embedding, embeddings, distance_metric="cosine"
    )
    indices_of_nearest_neighbors = utils.indices_of_nearest_neighbors_from_distances(distances)

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
    document = find_best_documents(query, documents, count=1)[0]
    raw_doc = data.iloc[document["index"]]
    return {
        "query_id": document["id"],
        "name": raw_doc["name"],
        "distance": document["distance"],
        "sql": raw_doc["query"],
    }
