from __future__ import annotations

import sys
from pathlib import Path

import grpc
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROJECT_ROOT / "generated"

if str(GENERATED_DIR) not in sys.path:
    sys.path.append(str(GENERATED_DIR))

import interview_pb2  # noqa: E402
import interview_pb2_grpc  # noqa: E402


def start_interview(
    track: str,
    level: str,
    mode: str,
) -> interview_pb2.StartInterviewResponse:
    channel: grpc.Channel = grpc.insecure_channel("localhost:50051")
    stub: interview_pb2_grpc.InterviewServiceStub = (
        interview_pb2_grpc.InterviewServiceStub(channel)
    )

    request: interview_pb2.StartInterviewRequest = interview_pb2.StartInterviewRequest(
        track=track,
        level=level,
        mode=mode,
    )

    response: interview_pb2.StartInterviewResponse = stub.StartInterview(request)

    return response


def submit_answer(session_id: str, answer: str) -> interview_pb2.SubmitAnswerResponse:
    channel: grpc.Channel = grpc.insecure_channel("localhost:50051")
    stub: interview_pb2_grpc.InterviewServiceStub = (
        interview_pb2_grpc.InterviewServiceStub(channel)
    )

    request: interview_pb2.SubmitAnswerRequest = interview_pb2.SubmitAnswerRequest(
        session_id=session_id,
        answer=answer,
    )

    response: interview_pb2.SubmitAnswerResponse = stub.SubmitAnswer(request)

    return response


st.set_page_config(
    page_title="Interview Simulator",
    page_icon="🎙️",
    layout="centered",
)

st.title("Interview Simulator")

st.write(
    "Тренажер технических собеседований. Выбери направление, уровень и формат интервью."
)

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None

if "is_finished" not in st.session_state:
    st.session_state.is_finished = False

track = st.selectbox(
    "Направление",
    ["Python", "Backend", "Machine Learning", "Data Engineering"],
)

level = st.selectbox(
    "Уровень",
    ["Junior", "Middle", "Senior"],
)

mode = st.radio(
    "Формат интервью",
    ["Theory", "Practice", "Mixed"],
)

if st.button("Начать интервью"):
    try:
        response: interview_pb2.StartInterviewResponse = start_interview(
            track=track,
            level=level,
            mode=mode,
        )

        st.session_state.session_id = response.session_id
        st.session_state.current_question = response.question
        st.session_state.last_feedback = None
        st.session_state.is_finished = False

    except grpc.RpcError as error:
        st.error("Не удалось подключиться к gRPC-серверу")
        st.code(str(error))

if st.session_state.current_question:
    st.subheader("Вопрос")
    st.write(st.session_state.current_question)

    answer = st.text_area("Твой ответ", height=140)

    if st.button("Отправить ответ"):
        if not answer.strip():
            st.warning("Сначала напиши ответ.")
        else:
            session_id = st.session_state.session_id

            if session_id is None:
                st.error("Сессия интервью не найдена")
            else:
                try:
                    response: interview_pb2.SubmitAnswerResponse = submit_answer(
                        session_id=session_id,
                        answer=answer,
                    )

                    st.session_state.last_feedback = response.feedback
                    st.session_state.is_finished = response.is_finished

                    if response.is_finished:
                        st.session_state.current_question = None
                    else:
                        st.session_state.current_question = response.next_question

                except grpc.RpcError as error:
                    st.error("Не удалось отправить ответ на gRPC-сервер")
                    st.code(str(error))

if st.session_state.last_feedback:
    st.subheader("Feedback")
    st.write(st.session_state.last_feedback)

if st.session_state.is_finished:
    st.success("Интервью завершено")
