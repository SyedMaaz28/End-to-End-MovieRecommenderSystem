from fastapi import APIRouter, Query
from app.ml.tfidf import tfidf_recommend_titles
from app.core.tmdb import tmdb_movie_details, tmdb_get, tmdb_cards_from_results
from app.models.schemas import TMDBMovieCard


router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.get("/tfidf")
def recommend_tfidf(title: str = Query(...), top_n: int = 10):
    recs = tfidf_recommend_titles(title, top_n)
    return [{"title": t, "score": s} for t, s in recs]


@router.get("/genre", response_model=list[TMDBMovieCard])
async def recommend_genre(
    tmdb_id: int,
    limit: int = 18,
):
    """
    Recommend movies based on first genre of given TMDB movie
    """
    details = await tmdb_movie_details(tmdb_id)

    if not details.genres:
        return []

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

    cards = await tmdb_cards_from_results(
        discover.get("results", []), limit
    )

    return [c for c in cards if c.tmdb_id != tmdb_id]
