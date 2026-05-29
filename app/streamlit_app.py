from pathlib import Path
import sys

import grpc
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROJECT_ROOT / "generated"

if str(GENERATED_DIR) not in sys.path:
    sys.path.append(str(GENERATED_DIR))

st.set_page_config(
    page_title="Interview simulator",
    page_icon="🎙️",
    layout="centered",
)

import interview_pb2
import interview_pb2_grpc

def start_interview(
        track: str,
        level: str,
        mode: str
) -> interview_pb2.StartInterviewResponse:
    channel: grpc.Channel = grpc.insecure_channel("localhost:50051")
    stud: interview_pb2_grpc.InterviewServiceStub = interview_pb2_grpc.InterviewServiceStub(channel)

    request: interview_pb2.StartInterviewRequest = interview_pb2.StartInterviewRequest(
        track=track,
        level=level,
        mode=mode,
    )

    response: interview_pb2.StartInterviewResponse = stud.StartInterview(request)

    return response

st.title("Interview simulator")

st.write(
    "Тренажер технических собеседований. "
    "Выбери направление, уровень и формат интервью."
)

track = st.selectbox(
    "Направление", 
    ["Python", "Backend", "Machine Learning", "Data Engineering"],
)

level = st.selectbox(
    "Grade", 
    ["junoir", "middle", "senior"]
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

        st.success("Интервью создано")
        st.caption(f"Session ID: {response.session_id}")
        st.subheader("Первый вопрос")
        st.write(response.question)

    except grpc.RpcError as error:
        st.error("Не удалось подключиться к gRPC-серверу")
        st.code(str(error))