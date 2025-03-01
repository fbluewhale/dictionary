from enum import Enum
from pymongo import MongoClient
from pydantic import BaseModel, Field, validator


class SupportedLanguage(Enum):
    FARSI = "fa"
    ENGLISH = "en"
    FRENCH = "fe"


class WordModel(BaseModel):
    word: str = Field(..., min_length=1)
    meanings: dict[str, str] 

    @validator("meanings")
    def validate_meanings(cls, v):
        if not all(
            isinstance(key, str) and isinstance(value, str) for key, value in v.items()
        ):
            raise ValueError("All keys and values in meanings must be strings.")
        return v

    def serialize(self) -> dict[str, str]:
        return {"word": self.word, "meanings": self.meanings}
