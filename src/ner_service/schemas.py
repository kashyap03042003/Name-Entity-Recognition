"""Request and response schemas for the NER API."""

from pydantic import BaseModel, ConfigDict, Field, field_validator

MAX_TEXT_LENGTH = 5_000


class PredictionRequest(BaseModel):
    """Text submitted for entity recognition."""

    model_config = ConfigDict(str_strip_whitespace=False)

    text: str = Field(min_length=1, max_length=MAX_TEXT_LENGTH)

    @field_validator("text")
    @classmethod
    def text_must_contain_non_whitespace(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text must contain at least one non-whitespace character")
        return value


class Entity(BaseModel):
    """A detected entity and its span in the original text."""

    text: str
    label: str
    start: int = Field(ge=0)
    end: int = Field(gt=0)


class PredictionResponse(BaseModel):
    """Entity recognition result for one input string."""

    text: str
    entities: list[Entity]

