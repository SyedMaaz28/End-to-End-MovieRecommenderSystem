import streamlit as st


def init_state():
    if "view" not in st.session_state:
        st.session_state.view = "home"
    if "selected_tmdb_id" not in st.session_state:
        st.session_state.selected_tmdb_id = None


def sync_query_params():
    qp_view = st.query_params.get("view")
    qp_id = st.query_params.get("id")

    if qp_view in ("home", "details"):
        st.session_state.view = qp_view

    if qp_id:
        try:
            st.session_state.selected_tmdb_id = int(qp_id)
            st.session_state.view = "details"
        except:
            pass


def goto_home():
    st.session_state.view = "home"
    st.query_params.clear()
    st.query_params["view"] = "home"
    st.rerun()


def goto_details(tmdb_id: int):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = int(tmdb_id)
    st.query_params["view"] = "details"
    st.query_params["id"] = str(tmdb_id)
    st.rerun()
