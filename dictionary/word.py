from models.words import WordModel


class WordCRUD:
    def __init__(self, db):
        self.db = db

    def create(self, new_word: str, meanings: dict[str, str]) -> bool:
        if not self.db.exists(new_word):
            word_entry = WordModel(word=new_word, meanings=meanings)
            self.db.write(word_entry.serialize())
            return True
        return False

    def get(self, key: str) -> str:
        result = self.db.get_or_none(key)
        if not result:
            raise Exception(f"The word '{key}' was not found!")
        return result

    def update(self, key: str, lang: str, definition) -> None:
        word = self.get(key)
        meanings = word.get("meanings", {})
        if isinstance(definition, dict):
            meanings.update(definition)
        else:
            meanings[lang] = definition
        self.db.update(key, {"meanings": meanings})
