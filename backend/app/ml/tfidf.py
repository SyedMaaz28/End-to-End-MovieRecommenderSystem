import numpy as np
from fastapi import HTTPException
from typing import List, Tuple

from .loader import df, tfidf_matrix, TITLE_TO_IDX


def tfidf_recommend_titles(title: str, top_n: int = 10) -> List[Tuple[str, float]]:
    if TITLE_TO_IDX is None:
        raise HTTPException(status_code=500, detail="TF-IDF not initialized")

    key = title.strip().lower()
    if key not in TITLE_TO_IDX:
        raise HTTPException(status_code=404, detail="Title not found")

    idx = TITLE_TO_IDX[key]
    qv = tfidf_matrix[idx]
    scores = (tfidf_matrix @ qv.T).toarray().ravel()

    order = np.argsort(-scores)

    out = []
    for i in order:
        if i == idx:
            continue
        out.append((df.iloc[i]["title"], float(scores[i])))
        if len(out) >= top_n:
            break

    return out
