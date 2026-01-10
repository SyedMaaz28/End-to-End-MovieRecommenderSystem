from fastapi import APIRouter
from app.core.tmdb import tmdb_movie_details
from app.models.schemas import TMDBMovieDetails

from fastapi import Query, HTTPException
from app.ml.tfidf import tfidf_recommend_titles
from app.core.tmdb import (
    tmdb_search_first,
    tmdb_cards_from_results,
    tmdb_get,
)
from app.models.schemas import (
    SearchBundleResponse,
    TFIDFRecItem,
    TMDBMovieCard,
)


router = APIRouter(prefix="/movie", tags=["movie"])

@router.get("/id/{tmdb_id}", response_model=TMDBMovieDetails)
async def movie_details(tmdb_id: int):
    return await tmdb_movie_details(tmdb_id)



@router.get("/search", response_model=SearchBundleResponse)
async def movie_search(
    query: str = Query(..., min_length=1),
    tfidf_top_n: int = 12,
    genre_limit: int = 12,
):
    """
    Bundle endpoint:
    - movie details
    - TF-IDF recommendations
    - genre-based recommendations
    """
    best = await tmdb_search_first(query)
    if not best:
        raise HTTPException(
            status_code=404, detail=f"No movie found for query: {query}"
        )

    tmdb_id = best["id"]
    details = await tmdb_movie_details(tmdb_id)

    # TF-IDF recommendations
    tfidf_items = []
    try:
        recs = tfidf_recommend_titles(details.title, tfidf_top_n)
    except Exception:
        recs = []

    for title, score in recs:
        tfidf_items.append(
            TFIDFRecItem(title=title, score=score, tmdb=None)
        )

    # Genre recommendations
    genre_recs = []
    if details.genres:
        genre_id = details.genres[0]["id"]
        discover = await tmdb_get(
            "/discover/movie",
            {
                "with_genres": genre_id,
                "language": "en-US",
                "sort_by": "popularity.desc",
                "page": 1,
            },
        )
        genre_recs = await tmdb_cards_from_results(
            discover.get("results", []), genre_limit
        )

    return SearchBundleResponse(
        query=query,
        movie_details=details,
        tfidf_recommendations=tfidf_items,
        genre_recommendations=genre_recs,
    )
