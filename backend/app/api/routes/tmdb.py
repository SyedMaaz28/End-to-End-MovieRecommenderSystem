from fastapi import APIRouter, Query
from app.core.tmdb import tmdb_get

router = APIRouter(prefix="/tmdb", tags=["tmdb"])


@router.get("/search")
async def tmdb_search(
    query: str = Query(..., min_length=1),
    page: int = Query(1, ge=1, le=10),
):
    """
    Raw TMDB search results (used for search/autocomplete)
    """
    return await tmdb_get(
        "/search/movie",
        {
            "query": query,
            "include_adult": "false",
            "language": "en-US",
            "page": page,
        },
    )
