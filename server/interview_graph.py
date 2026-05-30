from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class InterviewState(TypedDict, total=False):
    track: str
    level: str
    mode: str
    answer: str
    question_number: int
    question: str
    feedback: str
    next_question: str
    is_finished: bool


QUESTION_BANK: dict[tuple[str, str], list[str]] = {
    ("Python", "Junior"): [
        "Что происходит в Python, когда ты вызываешь функцию?",
        "Чем список отличается от кортежа?",
        "Что такое mutable и immutable типы?",
    ],
    ("Backend", "Junior"): [
        "Что происходит, когда браузер отправляет HTTP-запрос?",
        "Чем GET отличается от POST?",
        "Что такое статус-коды HTTP?",
    ],
}


def get_questions(track: str, level: str) -> list[str]:
    return QUESTION_BANK.get((track, level), QUESTION_BANK[("Python", "Junior")])


def create_first_question(state: InterviewState) -> InterviewState:
    questions: list[str] = get_questions(
        track=state["track"],
        level=state["level"],
    )

    return {
        "question_number": 0,
        "question": questions[0],
        "is_finished": False,
    }
