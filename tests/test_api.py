from fastapi.testclient import TestClient

from ner_service.api import create_app
from ner_service.schemas import Entity, PredictionResponse


class FakeRecognizer:
    def predict(self, text: str) -> PredictionResponse:
        return PredictionResponse(
            text=text,
            entities=[Entity(text="Ada", label="PERSON", start=0, end=3)],
        )


client = TestClient(create_app(recognizer=FakeRecognizer()))


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_returns_entity_and_offsets() -> None:
    response = client.post("/predict", json={"text": "Ada Lovelace"})

    assert response.status_code == 200
    assert response.json() == {
        "text": "Ada Lovelace",
        "entities": [
            {"text": "Ada", "label": "PERSON", "start": 0, "end": 3},
        ],
    }


def test_predict_rejects_blank_text() -> None:
    response = client.post("/predict", json={"text": "   "})

    assert response.status_code == 422


def test_predict_rejects_text_over_limit() -> None:
    response = client.post("/predict", json={"text": "a" * 5001})

    assert response.status_code == 422

