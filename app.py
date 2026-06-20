import streamlit as st
import csv
import os
import hashlib
from quiz_ui import render_quiz, reset_quiz_state, start_quiz
from dashboard_ui import render_dashboard
from leaderboard import render_leaderboard, render_my_history


USERS_FILE = "users.csv"
USER_FIELDS = ["username", "email", "password_hash"]


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=USER_FIELDS)
            writer.writeheader()


def load_users():
    create_users_file()

    with open(USERS_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def save_user(username, email, password):
    create_users_file()

    with open(USERS_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=USER_FIELDS)
        writer.writerow({
            "username": username,
            "email": email,
            "password_hash": hash_password(password)
        })


def find_user(username):
    users = load_users()

    for user in users:
        if user["username"] == username:
            return user

    return None


st.set_page_config(
    page_title="Quiz Game with Score Report",
    page_icon="🧠"
)

st.title("Quiz Game with Score Report")

st.warning("Toy project only. Do not use your real password.")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "email" not in st.session_state:
    st.session_state.email = ""

if "selected_level" not in st.session_state:
    st.session_state.selected_level = ""

if "level_selected" not in st.session_state:
    st.session_state.level_selected = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "dashboard"


if not st.session_state.logged_in:
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        st.subheader("Login")

        login_username = st.text_input(
            "Username",
            key="login_username"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login", key="login_button"):
            user = find_user(login_username)

            if user is None:
                st.error("Username not found. Please register first.")

            elif user["password_hash"] != hash_password(login_password):
                st.error("Wrong password.")

            else:
                st.session_state.logged_in = True
                st.session_state.username = user["username"]
                st.session_state.email = user["email"]
                st.session_state.current_page = "dashboard"
                st.success("Login successful.")
                st.rerun()    

    with register_tab:
        st.subheader("Register")

        register_username = st.text_input(
            "Create username",
            key="register_username"
        )

        register_email = st.text_input(
            "Email",
            key="register_email"
        )

        register_password = st.text_input(
            "Create password",
            type="password",
            key="register_password"
        )

        if st.button("Register", key="register_button"):
            if register_username.strip() == "":
                st.warning("Please enter a username.")

            elif register_email.strip() == "":
                st.warning("Please enter an email.")

            elif register_password.strip() == "":
                st.warning("Please enter a password.")

            elif find_user(register_username) is not None:
                st.error("This username already exists. Try another one.")

            else:
                save_user(register_username, register_email, register_password)
                st.success("Account created. Go to Login tab.")

else:
    with st.sidebar:
        st.write(f"User: {st.session_state.username}")

        if st.button("Dashboard", key="nav_dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()

        if st.button("Start Quiz", key="nav_start_quiz"):
            st.session_state.current_page = "level"
            st.rerun()

        if st.button("Leaderboard", key="nav_leaderboard"):
            st.session_state.current_page = "leaderboard"
            st.rerun()

        if st.button("My History", key="nav_history"):
            st.session_state.current_page = "history"
            st.rerun()

        if st.button("Logout", key="logout_button"):
            reset_quiz_state()
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.email = ""
            st.session_state.selected_level = ""
            st.session_state.level_selected = False
            st.session_state.current_page = "dashboard"
            st.rerun()

    if st.session_state.current_page == "dashboard":
        render_dashboard()

    elif st.session_state.current_page == "level":
        st.title("Choose Quiz Level")

        st.write(f"Username: {st.session_state.username}")
        st.write(f"Email: {st.session_state.email}")

        level = st.selectbox(
            "Select your quiz level:",
            ["Easy", "Medium", "Hard"],
            key="level_selectbox"
        )

        if level == "Easy":
            st.info("Easy: Basic Python questions. Good for warm-up.")
        elif level == "Medium":
            st.info("Medium: Loops, functions, lists, dictionaries, and files.")
        else:
            st.info("Hard: Code output, exceptions, decorators, JSON, and APIs.")

        if st.button("Start Quiz", key="start_quiz_button"):
            st.session_state.selected_level = level
            st.session_state.level_selected = True
            start_quiz()

    elif st.session_state.current_page == "quiz":
        render_quiz()

    elif st.session_state.current_page == "leaderboard":
        st.title("Leaderboard")
        render_leaderboard()

    elif st.session_state.current_page == "history":
        st.title("My History")
        render_my_history(st.session_state.username)