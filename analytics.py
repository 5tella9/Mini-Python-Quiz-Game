import pandas as pd
import streamlit as st


def create_answer_dataframe(user_answers):
    rows = []

    for index, answer in enumerate(user_answers, start=1):
        rows.append({
            "Question": f"Q{index}",
            "Status": "Correct" if answer["is_correct"] else "Wrong",
            "Time (sec)": answer["time_taken"],
            "Your Answer": answer["selected"],
            "Correct Answer": answer["correct"]
        })

    return pd.DataFrame(rows)


def render_analytics_report(user_answers):
    st.subheader("Enhanced Report & Analytics")

    df = create_answer_dataframe(user_answers)

    correct_count = len(df[df["Status"] == "Correct"])
    wrong_count = len(df[df["Status"] == "Wrong"])

    summary_df = pd.DataFrame({
        "Result": ["Correct", "Wrong"],
        "Count": [correct_count, wrong_count]
    })

    col1, col2 = st.columns(2)

    with col1:
        st.write("Correct vs Wrong")

        chart_df = summary_df.set_index("Result")

        st.bar_chart(
            chart_df,
            height=260,
            width="stretch"
        )

    with col2:
        st.write("Time Per Question")

        time_df = df[["Question", "Time (sec)"]].set_index("Question")

        st.bar_chart(
            time_df,
            height=260,
            width="stretch"
        )

    fastest_question = df.loc[df["Time (sec)"].idxmin()]
    slowest_question = df.loc[df["Time (sec)"].idxmax()]

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "Fastest Question",
            f"{fastest_question['Question']} - {fastest_question['Time (sec)']} sec"
        )

    with col4:
        st.metric(
            "Slowest Question",
            f"{slowest_question['Question']} - {slowest_question['Time (sec)']} sec"
        )

    st.write("Detailed Answer Table")

    st.dataframe(
        df,
        width="stretch",
        hide_index=True
    )