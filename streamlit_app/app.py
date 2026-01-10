import streamlit as st

from api.client import api_get_json
from state.router import (
    init_state,
    sync_query_params,
    goto_home,
)
from ui.styles import inject_styles
from ui.grids import poster_grid
from ui.helpers import (
    parse_tmdb_search_to_cards,
    to_cards_from_tfidf_items,
)

# -----------------------
# Init
# -----------------------
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
inject_styles()
init_state()
sync_query_params()

# -----------------------
# Sidebar
# -----------------------
with st.sidebar:
    st.markdown("## 🎬 Menu")
    if st.button("🏠 Home"):
        goto_home()

    st.markdown("---")
    home_category = st.selectbox(
        "Home Feed",
        ["trending", "popular", "top_rated", "now_playing", "upcoming"],
        index=0,
    )
    grid_cols = st.slider("Grid columns", 4, 8, 5)

# -----------------------
# Header
# -----------------------
st.title("🎬 Movie Recommender")
st.caption("Search → select → details → recommendations")
st.divider()

# -----------------------
# HOME VIEW
# -----------------------
if st.session_state.view == "home":
    typed = st.text_input("Search movie title")

    if typed.strip():
        data, err = api_get_json("/tmdb/search", {"query": typed})
        if not err and data:
            suggestions, cards = parse_tmdb_search_to_cards(data, typed)
            poster_grid(cards, cols=grid_cols, key_prefix="search")
        st.stop()

    cards, err = api_get_json("/home", {"category": home_category, "limit": 24})
    if not err:
        poster_grid(cards, cols=grid_cols, key_prefix="home")

# -----------------------
# DETAILS VIEW
# -----------------------
else:
    tmdb_id = st.session_state.selected_tmdb_id
    data, err = api_get_json(f"/movie/id/{tmdb_id}")
    if err:
        st.error(err)
        st.stop()

    left, right = st.columns([1, 2.4])
    with left:
        if data.get("poster_url"):
            st.image(data["poster_url"], use_column_width=True)

    with right:
        st.subheader(data["title"])
        st.write(data.get("overview", ""))

    bundle, _ = api_get_json("/movie/search", {"query": data["title"]})
    if bundle:
        st.subheader("🤖 Similar Movies - TFIDF Recommendations")
        poster_grid(
            to_cards_from_tfidf_items(bundle["tfidf_recommendations"]),
            cols=grid_cols,
            key_prefix="tfidf",
        )

        st.subheader("🎭 More Like This")
        poster_grid(
            bundle["genre_recommendations"],
            cols=grid_cols,
            key_prefix="genre",
        )
