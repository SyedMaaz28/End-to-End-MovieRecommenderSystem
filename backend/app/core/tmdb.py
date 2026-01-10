import httpx
from typing import Dict, Any, List, Optional
from fastapi import HTTPException

from .config import TMDB_API_KEY, TMDB_BASE, TMDB_IMG_500
from app.models.schemas import TMDBMovieCard, TMDBMovieDetails


def make_img_url(path: Optional[str]) -> Optional[str]:
    if not path:
        return None
    return f"{TMDB_IMG_500}{path}"


async def tmdb_get(path: str, params: Dict[str, Any]) -> Dict[str, Any]:
    q = dict(params)
    q["api_key"] = TMDB_API_KEY

    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(f"{TMDB_BASE}{path}", params=q)
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=str(e))

    if r.status_code != 200:
        raise HTTPException(status_code=502, detail=r.text)

    return r.json()


async def tmdb_cards_from_results(results: List[dict], limit: int = 20):
    cards = []
    for m in results[:limit]:
        cards.append(
            TMDBMovieCard(
                tmdb_id=int(m["id"]),
                title=m.get("title") or "",
                poster_url=make_img_url(m.get("poster_path")),
                release_date=m.get("release_date"),
                vote_average=m.get("vote_average"),
            )
        )
    return cards


async def tmdb_movie_details(movie_id: int) -> TMDBMovieDetails:
    data = await tmdb_get(f"/movie/{movie_id}", {"language": "en-US"})
    return TMDBMovieDetails(
        tmdb_id=int(data["id"]),
        title=data.get("title") or "",
        overview=data.get("overview"),
        release_date=data.get("release_date"),
        poster_url=make_img_url(data.get("poster_path")),
        backdrop_url=make_img_url(data.get("backdrop_path")),
        genres=data.get("genres", []),
    )


async def tmdb_search_first(query: str) -> dict | None:
    """
    Returns the first (best) TMDB search result for a query.
    Used by /movie/search bundle endpoint.
    """
    data = await tmdb_get(
        "/search/movie",
        {
            "query": query,
            "include_adult": "false",
            "language": "en-US",
            "page": 1,
        },
    )

    results = data.get("results", [])
    return results[0] if results else None
