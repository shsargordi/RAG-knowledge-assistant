from unittest.mock import patch

from fastapi.testclient import TestClient

from api import app
from pro_implementation.answer import Result

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_returns_answer_and_sources():
    fake_chunks = [Result(page_content="Avery is the CEO.", metadata={"source": "hr/avery.md"})]
    with patch("api.answer_question", return_value=("Avery Lancaster is the CEO.", fake_chunks)):
        response = client.post("/ask", json={"question": "Who is Avery?"})
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Avery Lancaster is the CEO."
    assert data["sources"] == ["hr/avery.md"]
