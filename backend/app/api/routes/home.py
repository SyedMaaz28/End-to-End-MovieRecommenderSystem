from fastapi import APIRouter, Query, HTTPException
from app.core.tmdb import tmdb_get, tmdb_cards_from_results
from app.models.schemas import TMDBMovieCard

router = APIRouter(tags=["home"])


@router.get("/home", response_model=list[TMDBMovieCard])
async def home(
    category: str = Query("popular"),
    limit: int = Query(24, ge=1, le=50),
):
    """
    Home feed movies
    category:
      - trending
      - popular
      - top_rated
      - upcoming
      - now_playing
    """
    if category == "trending":
        data = await tmdb_get("/trending/movie/day", {"language": "en-US"})
        return await tmdb_cards_from_results(data.get("results", []), limit)

    if category not in {"popular", "top_rated", "upcoming", "now_playing"}:
        raise HTTPException(status_code=400, detail="Invalid category")

    try:
        data = await tmdb_get(
            f"/movie/{category}",
            {"language": "en-US", "page": 1},
        )
        return await tmdb_cards_from_results(
            data.get("results", []), limit=limit
        )

    except Exception as e:
    # Log but don't crash
        print(f"[HOME] TMDB failed: {e}")
        return []
