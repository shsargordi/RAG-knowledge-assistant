from fastapi import FastAPI
from pydantic import BaseModel

from pro_implementation.answer import answer_question

app = FastAPI(title="RAG Knowledge Assistant API")


class AskRequest(BaseModel):
    question: str
    history: list[dict] = []


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    answer, chunks = answer_question(request.question, request.history)
    sources = [chunk.metadata.get("source", "") for chunk in chunks]
    return AskResponse(answer=answer, sources=sources)
