from config import TMDB_IMG


def to_cards_from_tfidf_items(tfidf_items):
    cards = []
    for x in tfidf_items or []:
        tmdb = x.get("tmdb") or {}
        if tmdb.get("tmdb_id"):
            cards.append(
                {
                    "tmdb_id": tmdb["tmdb_id"],
                    "title": tmdb.get("title") or x.get("title") or "Untitled",
                    "poster_url": tmdb.get("poster_url"),
                }
            )
    return cards


def parse_tmdb_search_to_cards(data, keyword: str, limit: int = 24):
    keyword_l = keyword.strip().lower()
    raw_items = []

    if isinstance(data, dict) and "results" in data:
        for m in data.get("results") or []:
            if m.get("id") and m.get("title"):
                raw_items.append(
                    {
                        "tmdb_id": int(m["id"]),
                        "title": m["title"],
                        "poster_url": f"{TMDB_IMG}{m['poster_path']}"
                        if m.get("poster_path")
                        else None,
                        "release_date": m.get("release_date", ""),
                    }
                )

    elif isinstance(data, list):
        for m in data:
            if m.get("tmdb_id") and m.get("title"):
                raw_items.append(m)

    matched = [x for x in raw_items if keyword_l in x["title"].lower()]
    final_list = matched if matched else raw_items

    suggestions = []
    for x in final_list[:10]:
        year = (x.get("release_date") or "")[:4]
        label = f"{x['title']} ({year})" if year else x["title"]
        suggestions.append((label, x["tmdb_id"]))

    cards = final_list[:limit]
    return suggestions, cards
