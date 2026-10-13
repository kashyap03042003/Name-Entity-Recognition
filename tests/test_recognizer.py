from spacy.tokens import Doc
from spacy.vocab import Vocab

from ner_service.recognizer import EntityRecognizer


def test_predict_returns_spans_and_preserves_input_text() -> None:
    text = "Ada Lovelace"
    doc = Doc(
        Vocab(),
        words=["Ada", "Lovelace"],
        spaces=[True, False],
        ents=["B-PERSON", "I-PERSON"],
    )
    recognizer = EntityRecognizer(nlp=lambda _: doc)  # type: ignore[arg-type]

    result = recognizer.predict(text)

    assert result.text == text
    assert [entity.model_dump() for entity in result.entities] == [
        {"text": "Ada Lovelace", "label": "PERSON", "start": 0, "end": 12},
    ]

