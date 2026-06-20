import time
import streamlit as st
from questions import get_questions
from analytics import render_analytics_report
from leaderboard import save_score, render_leaderboard

QUESTION_TIME_LIMIT = 30


def init_quiz_state():
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False

    if "current_question" not in st.session_state:
        st.session_state.current_question = 0

    if "score" not in st.session_state:
        st.session_state.score = 0

    if "user_answers" not in st.session_state:
        st.session_state.user_answers = []

    if "answer_submitted" not in st.session_state:
        st.session_state.answer_submitted = False

    if "quiz_finished" not in st.session_state:
        st.session_state.quiz_finished = False

    if "quiz_start_time" not in st.session_state:
        st.session_state.quiz_start_time = None

    if "question_start_time" not in st.session_state:
        st.session_state.question_start_time = None

    if "time_expired" not in st.session_state:
        st.session_state.time_expired = False
    
    if "result_saved" not in st.session_state:
        st.session_state.result_saved = False


def reset_quiz_state():
    st.session_state.quiz_started = False
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.user_answers = []
    st.session_state.answer_submitted = False
    st.session_state.quiz_finished = False
    st.session_state.quiz_start_time = None
    st.session_state.question_start_time = None
    st.session_state.time_expired = False
    st.session_state.result_saved = False

    for key in list(st.session_state.keys()):
        if key.startswith("answer_"):
            del st.session_state[key]


def start_quiz():
    reset_quiz_state()
    st.session_state.quiz_started = True
    st.session_state.quiz_start_time = time.time()
    st.session_state.question_start_time = time.time()
    st.session_state.current_page = "quiz"
    st.rerun()


def get_time_taken():
    if st.session_state.question_start_time is None:
        return 0

    return round(time.time() - st.session_state.question_start_time, 2)


def save_answer(question, selected_answer):
    correct_answer = question["answer"]
    is_correct = selected_answer == correct_answer
    time_taken = get_time_taken()

    if is_correct:
        st.session_state.score += 1

    st.session_state.user_answers.append({
        "question": question["question"],
        "selected": selected_answer,
        "correct": correct_answer,
        "is_correct": is_correct,
        "time_taken": time_taken
    })

    st.session_state.answer_submitted = True


def save_timeout_answer(question):
    time_taken = QUESTION_TIME_LIMIT

    st.session_state.user_answers.append({
        "question": question["question"],
        "selected": "No answer - time up",
        "correct": question["answer"],
        "is_correct": False,
        "time_taken": time_taken
    })

    st.session_state.answer_submitted = True
    st.session_state.time_expired = False


@st.fragment(run_every="1s")
def render_countdown_timer():
    if st.session_state.answer_submitted:
        return

    if st.session_state.quiz_finished:
        return

    if st.session_state.question_start_time is None:
        return

    elapsed_time = int(time.time() - st.session_state.question_start_time)
    remaining_time = max(0, QUESTION_TIME_LIMIT - elapsed_time)

    st.metric("Time Left", f"{remaining_time} seconds")
    st.progress(remaining_time / QUESTION_TIME_LIMIT)

    if remaining_time <= 0:
        st.session_state.time_expired = True
        st.rerun()


def go_to_next_question():
    st.session_state.current_question += 1
    st.session_state.answer_submitted = False
    st.session_state.question_start_time = time.time()
    st.session_state.time_expired = False
    st.rerun()


def render_quiz():
    init_quiz_state()

    questions = get_questions(st.session_state.selected_level)
    total_questions = len(questions)
    question_index = st.session_state.current_question
    question = questions[question_index]

    st.title("Quiz Page")
    st.caption(f"Level: {st.session_state.selected_level}")

    if st.button("Back to Level Selection"):
        reset_quiz_state()
        st.session_state.current_page = "level"
        st.rerun()

    st.divider()

    if st.session_state.quiz_finished:
        show_quiz_review(questions)
        return

    if st.session_state.time_expired and not st.session_state.answer_submitted:
        save_timeout_answer(question)
        st.rerun()

    st.subheader(f"Question {question_index + 1} of {total_questions}")
    st.progress((question_index + 1) / total_questions)

    render_countdown_timer()

    st.write(question["question"])

    answer_key = f"answer_{question_index}"

    selected_answer = st.radio(
        "Choose your answer:",
        question["options"],
        index=None,
        key=answer_key
    )

    if not st.session_state.answer_submitted:
        if st.button("Submit Answer", key=f"submit_{question_index}"):
            if selected_answer is None:
                st.warning("Please choose an answer first.")
            else:
                save_answer(question, selected_answer)
                st.rerun()

    else:
        last_answer = st.session_state.user_answers[-1]

        if last_answer["selected"] == "No answer - time up":
            st.error("Time is up.")
            st.info(f"Correct answer: {last_answer['correct']}")
        elif last_answer["is_correct"]:
            st.success("Correct!")
        else:
            st.error(f"Wrong. Correct answer: {last_answer['correct']}")

        st.write(f"Time taken: {last_answer['time_taken']} seconds")

        if question_index < total_questions - 1:
            if st.button("Next Question", key=f"next_{question_index}"):
                go_to_next_question()
        else:
            if st.button("Finish Quiz", key="finish_quiz_button"):
                st.session_state.quiz_finished = True
                st.rerun()


def show_quiz_review(questions):
    total_questions = len(questions)
    score = st.session_state.score
    percentage = round((score / total_questions) * 100, 2)

    total_time = sum(answer["time_taken"] for answer in st.session_state.user_answers)
    total_time = round(total_time, 2)

    average_time = round(total_time / total_questions, 2)

    if not st.session_state.result_saved:
        save_score(
            username=st.session_state.username,
            email=st.session_state.email,
            level=st.session_state.selected_level,
            score=score,
            total_questions=total_questions,
            percentage=percentage,
            total_time=total_time,
            average_time=average_time
        )

        st.session_state.result_saved = True
    st.title("Result Page")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Score", f"{score}/{total_questions}")

    with col2:
        st.metric("Percentage", f"{percentage}%")

    with col3:
        st.metric("Total Time", f"{total_time} sec")

    st.metric("Average Time Per Question", f"{average_time} sec")

    if percentage >= 80:
        st.success("Great job.")
    elif percentage >= 50:
        st.warning("Good try. Review the wrong answers.")
    else:
        st.error("You need more practice.")

    render_analytics_report(st.session_state.user_answers)

    render_leaderboard()

    st.subheader("Answer Review")

    for index, answer_data in enumerate(st.session_state.user_answers, start=1):
        with st.expander(f"Question {index}"):
            st.write(answer_data["question"])
            st.write(f"Your answer: {answer_data['selected']}")
            st.write(f"Correct answer: {answer_data['correct']}")
            st.write(f"Time taken: {answer_data['time_taken']} seconds")

            if answer_data["is_correct"]:
                st.success("Correct")
            else:
                st.error("Wrong")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Try Again"):
            reset_quiz_state()
            st.session_state.quiz_started = True
            st.session_state.quiz_start_time = time.time()
            st.session_state.question_start_time = time.time()
            st.rerun()

    with col2:
        if st.button("Choose Another Level"):
            reset_quiz_state()
            st.session_state.current_page = "level"
            st.rerun()