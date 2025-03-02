from db.database import *
from dictionary.tie import Trie
from dictionary.word import WordCRUD


class Dictionary:
    def __init__(self, db):
        self.db = db
        self.trie = Trie()
        self.update_trie()
        self.crud = WordCRUD(db)

    def write(self, new_word: str, meanings: dict[str, str]) -> bool:
        """
        Adds a new word with its meanings to the database.
        meanings: A dictionary with language keys ("fa", "en", "fe") and their respective translations.
        """
        creations_response = self.crud.create(new_word=new_word, meanings=meanings)
        if creations_response:
            self.update_trie()
        return creations_response

    def read(self, key: str, lang: str) -> str:
        """
        Fetches the meaning of a word in the specified language.
        key: The word to lookup.
        lang: The language in which to retrieve the meaning.
        """
        word = self.crud.get(key)
        meaning = word.get("meanings", {}).get(lang)
        if not meaning:
            raise Exception(f"The word '{key}' does not have a definition in {lang}.")
        return meaning

    def update(self, key: str, lang: str, definition) -> None:
        update_status = self.crud.update(key, lang, definition)
        if update_status:
            self.update_trie()

    def update_trie_with_list_data(self, data: list, trie):
        for doc in data:
            word = doc.get("word")
            if word:
                trie.insert(word)

    def update_trie_with_dict_data(self, data: list, trie):
        for word in data.keys():
            trie.insert(word)

    def update_trie(self):
        trie = self.trie
        data = self.db.get_whole_data()
        if isinstance(data, list):
            self.update_trie_with_list_data(data, trie)
        elif isinstance(data, dict):
            self.update_trie_with_dict_data(data, trie)

    def search(self, prefix: str) -> list[str]:
        return self.trie.starts_with(prefix)
