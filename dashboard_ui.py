import streamlit as st


def change_page(page_name):
    st.session_state.current_page = page_name
    st.rerun()


def render_dashboard():
    st.title("Dashboard")

    st.write(f"Welcome, {st.session_state.username}")
    st.write("Choose what you want to do.")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Start Quiz", use_container_width=True):
            change_page("level")

    with col2:
        if st.button("Leaderboard", use_container_width=True):
            change_page("leaderboard")

    with col3:
        if st.button("My History", use_container_width=True):
            change_page("history")

    st.divider()

    st.subheader("Project Features")

    st.write("✅ Login and register system")
    st.write("✅ Level selection")
    st.write("✅ One-question-per-page quiz")
    st.write("✅ Countdown timer")
    st.write("✅ Score report")
    st.write("✅ Analytics charts")
    st.write("✅ Leaderboard")