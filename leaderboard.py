import csv
import os
from datetime import datetime

import pandas as pd
import streamlit as st


LEADERBOARD_FILE = "leaderboard.csv"

LEADERBOARD_FIELDS = [
    "username",
    "email",
    "level",
    "score",
    "total_questions",
    "percentage",
    "total_time",
    "average_time",
    "date_time"
]


def create_leaderboard_file():
    if not os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=LEADERBOARD_FIELDS)
            writer.writeheader()


def save_score(username, email, level, score, total_questions, percentage, total_time, average_time):
    create_leaderboard_file()

    with open(LEADERBOARD_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=LEADERBOARD_FIELDS)
        writer.writerow({
            "username": username,
            "email": email,
            "level": level,
            "score": score,
            "total_questions": total_questions,
            "percentage": percentage,
            "total_time": total_time,
            "average_time": average_time,
            "date_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })


def load_leaderboard():
    create_leaderboard_file()

    df = pd.read_csv(LEADERBOARD_FILE)

    if df.empty:
        return df

    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["total_questions"] = pd.to_numeric(df["total_questions"], errors="coerce")
    df["percentage"] = pd.to_numeric(df["percentage"], errors="coerce")
    df["total_time"] = pd.to_numeric(df["total_time"], errors="coerce")
    df["average_time"] = pd.to_numeric(df["average_time"], errors="coerce")

    return df


def render_leaderboard():
    st.subheader("Leaderboard")

    df = load_leaderboard()

    if df.empty:
        st.info("No leaderboard data yet.")
        return

    sorted_df = df.sort_values(
        by=["score", "percentage", "total_time"],
        ascending=[False, False, True]
    )

    top_df = sorted_df.head(10)
    top_df=top_df.drop(columns=["email"], errors="ignore")
    
    st.dataframe(
        top_df,
        use_container_width=True,
        hide_index=True
    )

def render_my_history(username):
    st.subheader("My Quiz History")

    df = load_leaderboard()

    if df.empty:
        st.info("You have no quiz history yet.")
        return

    user_df = df[df["username"] == username]

    if user_df.empty:
        st.info("You have no quiz history yet.")
        return

    user_df = user_df.sort_values(
        by="date_time",
        ascending=False
    )

    best_score = user_df["score"].max()
    best_percentage = user_df["percentage"].max()
    attempts = len(user_df)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Attempts", attempts)

    with col2:
        st.metric("Best Score", best_score)

    with col3:
        st.metric("Best Percentage", f"{best_percentage}%")

    st.dataframe(
        user_df,
        use_container_width=True,
        hide_index=True
    )