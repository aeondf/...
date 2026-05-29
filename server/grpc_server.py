from concurrent import futures
from pathlib import Path
import sys
import uuid

import grpc

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROJECT_ROOT / "generated"

if str(GENERATED_DIR) not in sys.path:
    sys.path.append(str(GENERATED_DIR))

import interview_pb2
import interview_pb2_grpc


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

        return interview_pb2.StartInterviewResponse(
            session_id=session_id,
            question=question,
        )


def serve() -> None:
    server: grpc.Server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

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
