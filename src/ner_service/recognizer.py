"""spaCy-backed named entity recognition."""

from functools import lru_cache
import os

import spacy
from spacy.language import Language

from ner_service.schemas import Entity, PredictionResponse

DEFAULT_MODEL = "en_core_web_sm"


class EntityRecognizer:
    """Extract named entities with a loaded spaCy language pipeline."""

    def __init__(self, nlp: Language) -> None:
        self._nlp = nlp

    @classmethod
    def load(cls, model_name: str = DEFAULT_MODEL) -> "EntityRecognizer":
        """Load an installed spaCy model by package name or path."""
        return cls(spacy.load(model_name))

    def predict(self, text: str) -> PredictionResponse:
        """Return recognized entities with offsets into the input text."""
        doc = self._nlp(text)
        entities = [
            Entity(
                text=span.text,
                label=span.label_,
                start=span.start_char,
                end=span.end_char,
            )
            for span in doc.ents
        ]
        return PredictionResponse(text=text, entities=entities)


@lru_cache(maxsize=2)
def _load_model(model_name: str) -> EntityRecognizer:
    return EntityRecognizer.load(model_name)


def get_recognizer() -> EntityRecognizer:
    """Return a cached recognizer for the configured spaCy model."""
    model_name = os.getenv("NER_MODEL", DEFAULT_MODEL)
    return _load_model(model_name)

