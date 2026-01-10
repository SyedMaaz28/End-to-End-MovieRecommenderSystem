import os
import pickle
import pandas as pd

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../")
)

ARTIFACTS_DIR = os.path.join(PROJECT_ROOT, "ml", "artifacts")

df = None
indices = None
tfidf = None
tfidf_matrix = None
TITLE_TO_IDX = None


def _norm_title(t: str) -> str:
    return t.strip().lower()


def load_pickles():
    global df, indices, tfidf, tfidf_matrix, TITLE_TO_IDX

    with open(os.path.join(ARTIFACTS_DIR, "df.pkl"), "rb") as f:
        df = pickle.load(f)

    with open(os.path.join(ARTIFACTS_DIR, "indices.pkl"), "rb") as f:
        indices = pickle.load(f)

    with open(os.path.join(ARTIFACTS_DIR, "tfidf.pkl"), "rb") as f:
        tfidf = pickle.load(f)

    with open(os.path.join(ARTIFACTS_DIR, "tfidf_matrix.pkl"), "rb") as f:
        tfidf_matrix = pickle.load(f)

    TITLE_TO_IDX = {_norm_title(k): int(v) for k, v in indices.items()}
