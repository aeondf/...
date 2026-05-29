from __future__ import annotations

import sys
from pathlib import Path

import grpc

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROJECT_ROOT / "generated"

if str(GENERATED_DIR) not in sys.path:
    sys.path.append(str(GENERATED_DIR))

import interview_pb2  # noqa: E402
import interview_pb2_grpc  # noqa: E402


def main() -> None:
    channel: grpc.Channel = grpc.insecure_channel("localhost:50051")
    stub: interview_pb2_grpc.InterviewServiceStub = (
        interview_pb2_grpc.InterviewServiceStub(channel)
    )

    start_request: interview_pb2.StartInterviewRequest = (
        interview_pb2.StartInterviewRequest(
            track="Python",
            level="Junior",
            mode="Theory",
        )
    )

    start_response: interview_pb2.StartInterviewResponse = stub.StartInterview(
        start_request
    )

    print(f"Session ID: {start_response.session_id}")
    print(f"Question: {start_response.question}")

    answer_request: interview_pb2.SubmitAnswerRequest = (
        interview_pb2.SubmitAnswerRequest(
            session_id=start_response.session_id,
            answer=(
                "Когда вызывается функция, Python создает новый frame, "
                "передает туда аргументы, выполняет тело функции "
                "и возвращает результат."
            ),
        )
    )

    answer_response: interview_pb2.SubmitAnswerResponse = stub.SubmitAnswer(
        answer_request
    )

    print(f"Feedback: {answer_response.feedback}")
    print(f"Next question: {answer_response.next_question}")
    print(f"Is finished: {answer_response.is_finished}")


if __name__ == "__main__":
    main()
