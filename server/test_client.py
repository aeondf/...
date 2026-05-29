from pathlib import Path
import sys

import grpc

PROJECT_ROOT = Path(__file__).resolve().parents[1]
GENERATED_DIR = PROJECT_ROOT / "generated"

if str(GENERATED_DIR) not in sys.path:
    sys.path.append(str(GENERATED_DIR))

import interview_pb2
import interview_pb2_grpc


def main() -> None:
    channel: grpc.Channel = grpc.insecure_channel("localhost:50051")
    stub: interview_pb2_grpc.InterviewServiceStub = (
        interview_pb2_grpc.InterviewServiceStub(channel)
    )

    request: interview_pb2.StartInterviewRequest = interview_pb2.StartInterviewRequest(
        track="Python",
        level="Junior",
        mode="Theory",
    )

    response: interview_pb2.StartInterviewResponse = stub.StartInterview(request)

    print(f"Session ID: {response.session_id}")
    print(f"Question: {response.question}")


if __name__ == "__main__":
    main()
