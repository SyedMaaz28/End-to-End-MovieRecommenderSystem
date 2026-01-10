import os
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "/..")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
ARTIFACTS_DIR = os.path.join(PROJECT_ROOT, "ml", "artifacts")

os.makedirs(ARTIFACTS_DIR, exist_ok=True)

# Load data
df = pd.read_csv(os.path.join(DATA_DIR, "tmdb_movies.csv"),low_memory=False)
df["overview"] = df["overview"].fillna("")
df["title"] = df["title"].astype(str)
df = df.reset_index(drop=True)

# TF-IDF
tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=5000,
    ngram_range=(1, 2),
)
tfidf_matrix = tfidf.fit_transform(df["overview"])

# Indices
indices = pd.Series(df.index, index=df["title"]).drop_duplicates()

# Save artifacts
with open(os.path.join(ARTIFACTS_DIR, "df.pkl"), "wb") as f:
    pickle.dump(df, f)

with open(os.path.join(ARTIFACTS_DIR, "indices.pkl"), "wb") as f:
    pickle.dump(indices, f)

with open(os.path.join(ARTIFACTS_DIR, "tfidf.pkl"), "wb") as f:
    pickle.dump(tfidf, f)

with open(os.path.join(ARTIFACTS_DIR, "tfidf_matrix.pkl"), "wb") as f:
    pickle.dump(tfidf_matrix, f)

print("✅ Artifacts generated locally")
