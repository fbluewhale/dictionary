from db.database import *
from dictionary.tie import Trie
from models.words import WordModel


class Dictionary:
    def __init__(self, db):
        self.db = db
        self.trie = Trie()
        self.update_trie()

    def write(self, new_word: str, meanings: dict[str, str]) -> bool:
        """
        Adds a new word with its meanings to the database.
        meanings: A dictionary with language keys ("fa", "en", "fe") and their respective translations.
        """
        if not self.db.exists(new_word):
            word_entry = WordModel(word=new_word, meanings=meanings)
            self.db.write(word_entry.serialize())
            self.update_trie()
            return True
        else:
            return False

    def read(self, key: str, lang: str) -> str:
        """
        Fetches the meaning of a word in the specified language.
        key: The word to lookup.
        lang: The language in which to retrieve the meaning.
        """
        result = self.db.get_or_none(key)

        if not result:
            raise Exception(f"The word '{key}' was not found!")

        meaning = result.get("meanings", {}).get(lang)

        if not meaning:
            raise Exception(f"The word '{key}' does not have a definition in {lang}.")

        return meaning

    def update(self, word: str, lang: str, definition) -> None:
        record = self.db.get_or_none(word)
        if not record:
            raise Exception(f"The word '{word}' does not exist!")
        meanings = record.get("meanings", {})
        if isinstance(definition, dict):
            meanings.update(definition)
        else:
            meanings[lang] = definition
        self.db.update(word, {"meanings": meanings})
        self.update_trie()

    def update_trie(self):
        trie = self.trie
        data = self.db.get_whole_data()
        if isinstance(data, list):
            for doc in data:
                word = doc.get("word")
                if word:
                    trie.insert(word)
        elif isinstance(data, dict):
            for word in data.keys():
                trie.insert(word)

    def search(self, prefix: str) -> list[str]:
        return self.trie.starts_with(prefix)
