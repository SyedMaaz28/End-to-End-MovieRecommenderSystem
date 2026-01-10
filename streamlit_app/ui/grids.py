import streamlit as st
from state.router import goto_details


def poster_grid(cards, cols=6, key_prefix="grid"):
    if not cards:
        st.info("No movies to show.")
        return

    rows = (len(cards) + cols - 1) // cols
    idx = 0

    for r in range(rows):
        colset = st.columns(cols)
        for c in range(cols):
            if idx >= len(cards):
                break

            m = cards[idx]
            idx += 1

            with colset[c]:
                if m.get("poster_url"):
                    st.image(m["poster_url"], use_column_width=True)
                else:
                    st.write("🖼️ No poster")

                if st.button(
                    "Open",
                    key=f"{key_prefix}_{r}_{c}_{idx}_{m.get('tmdb_id')}",
                ):
                    if m.get("tmdb_id"):
                        goto_details(m["tmdb_id"])

                st.markdown(
                    f"<div class='movie-title'>{m.get('title','')}</div>",
                    unsafe_allow_html=True,
                )
