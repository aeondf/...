from __future__ import annotations

import sys
import uuid
from concurrent import futures
from pathlib import Path

import grpc

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROJECT_ROOT / "generated"

if str(GENERATED_DIR) not in sys.path:
    sys.path.append(str(GENERATED_DIR))

import interview_pb2  # noqa: E402
import interview_pb2_grpc  # noqa: E402

type SessionData = dict[str, str]

SESSIONS: dict[str, SessionData] = {}


class InterviewService(interview_pb2_grpc.InterviewServiceServicer):
    def StartInterview(
        self,
        request: interview_pb2.StartInterviewRequest,
        context: grpc.ServicerContext,
    ) -> interview_pb2.StartInterviewResponse:
        session_id: str = str(uuid.uuid4())

        question: str = (
            f"Первый вопрос для {request.level} по направлению {request.track}: "
            "что происходит в Python, когда ты вызываешь функцию?"
        )

        SESSIONS[session_id] = {
            "track": request.track,
            "level": request.level,
            "mode": request.mode,
            "current_question": question,
        }

        return interview_pb2.StartInterviewResponse(
            session_id=session_id,
            question=question,
        )

    def SubmitAnswer(
        self,
        request: interview_pb2.SubmitAnswerRequest,
        context: grpc.ServicerContext,
    ) -> interview_pb2.SubmitAnswerResponse:
        session: SessionData | None = SESSIONS.get(request.session_id)

        if session is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "Session not found")

        answer: str = request.answer.strip()

        if len(answer) < 40:
            feedback: str = (
                "Ответ пока короткий. На интервью лучше раскрывать мысль подробнее "
                "и добавить пример."
            )
        else:
            feedback = (
                "Хорошее начало. Ответ выглядит осмысленным. "
                "Чтобы усилить его, добавь конкретный пример из кода."
            )

        next_question: str = "Чем список отличается от кортежа в Python"

        return interview_pb2.SubmitAnswerResponse(
            feedback=feedback,
            next_question=next_question,
            is_finished=False,
        )


def serve() -> None:
    server: grpc.Server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    interview_pb2_grpc.add_InterviewServiceServicer_to_server(
        InterviewService(),
        server,
    )

    server.add_insecure_port("[::]:50051")
    server.start()

    print("gRPC server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
