import streamlit as st


def inject_styles():
    st.markdown(
        """
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1400px; }
    .small-muted { color:#6b7280; font-size: 0.92rem; }
    .movie-title { font-size: 0.9rem; line-height: 1.15rem; height: 2.3rem; overflow: hidden; }
    .card { border: 1px solid rgba(0,0,0,0.08); border-radius: 16px; padding: 14px; background: rgba(255,255,255,0.7); }
    </style>
    """,
        unsafe_allow_html=True,
    )
