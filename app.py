from fastapi import FastAPI
from pydantic import BaseModel

from backend.assistant import answer_question

app = FastAPI(
    title="AI Shopping Assistant"
)


class Question(BaseModel):
    question: str


@app.get("/")
def home():

    return {
        "message": "AI Shopping Assistant API is running!"
    }


@app.post("/ask")
def ask(data: Question):

    return answer_question(data.question)