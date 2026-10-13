"""FastAPI application for named entity recognition."""

from typing import Protocol

from fastapi import FastAPI

from ner_service.recognizer import get_recognizer
from ner_service.schemas import PredictionRequest, PredictionResponse


class Recognizer(Protocol):
    """Interface required by the prediction route."""

    def predict(self, text: str) -> PredictionResponse: ...


def create_app(recognizer: Recognizer | None = None) -> FastAPI:
    """Create an API app, optionally injecting a recognizer for testing."""
    application = FastAPI(
        title="Named Entity Recognition API",
        description="Extract named entities from English text.",
        version="0.1.0",
    )

    @application.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @application.post(
        "/predict",
        response_model=PredictionResponse,
        tags=["prediction"],
    )
    def predict(request: PredictionRequest) -> PredictionResponse:
        active_recognizer = recognizer if recognizer is not None else get_recognizer()
        return active_recognizer.predict(request.text)

    return application


app = create_app()
