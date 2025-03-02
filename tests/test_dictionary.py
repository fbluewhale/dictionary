import pytest


class FakeDb:
    def __init__(self):
        self.data = {}

    def exists(self, key: str) -> bool:
        return key in self.data

    def get_or_none(self, key: str) -> dict:
        return self.data.get(key)

    def get_whole_data(self):
        return self.data

    def write(self, data: dict):
        self.data[data["word"]] = data

    def update(self, key: str, data: dict):
        if key in self.data:
            self.data[key].update(data)
        else:
            self.data[key] = data


from dictionary.dictionary import Dictionary


def test_write_new_word():
    db = FakeDb()
    dictionary = Dictionary(db)
    result = dictionary.write(
        "hello", {"en": "greeting", "fa": "سلام", "fe": "bonjour"}
    )
    assert result is True
    stored = db.get_or_none("hello")
    assert stored is not None
    assert stored["meanings"]["en"] == "greeting"


def test_write_existing_word():
    db = FakeDb()
    dictionary = Dictionary(db)
    dictionary.write("hello", {"en": "greeting", "fa": "سلام", "fe": "bonjour"})
    result = dictionary.write("hello", {"en": "hi", "fa": "سلام", "fe": "bonjour"})
    assert result is False


def test_read_existing_word():
    db = FakeDb()
    dictionary = Dictionary(db)
    dictionary.write("hello", {"en": "greeting", "fa": "سلام", "fe": "bonjour"})
    meaning = dictionary.read("hello", "en")
    assert meaning == "greeting"


def test_read_nonexistent_word():
    db = FakeDb()
    dictionary = Dictionary(db)
    with pytest.raises(Exception) as excinfo:
        dictionary.read("nonexistent", "en")
    assert "was not found" in str(excinfo.value)


def test_read_missing_language():
    db = FakeDb()
    dictionary = Dictionary(db)
    dictionary.write("hello", {"en": "greeting"})
    with pytest.raises(Exception) as excinfo:
        dictionary.read("hello", "fa")
    assert "does not have a definition" in str(excinfo.value)


def test_update_word_single_language():
    db = FakeDb()
    dictionary = Dictionary(db)
    dictionary.write("hello", {"en": "greeting", "fa": "سلام", "fe": "bonjour"})
    dictionary.update("hello", "en", "hi")
    updated_meaning = dictionary.read("hello", "en")
    assert updated_meaning == "hi"


def test_update_word_with_dict():
    db = FakeDb()
    dictionary = Dictionary(db)
    dictionary.write("hello", {"en": "greeting", "fa": "سلام", "fe": "bonjour"})
    dictionary.update("hello", "en", {"en": "hi", "fa": "درود"})
    assert dictionary.read("hello", "en") == "hi"
    assert dictionary.read("hello", "fa") == "درود"
    assert dictionary.read("hello", "fe") == "bonjour"


def test_update_nonexistent_word():
    db = FakeDb()
    dictionary = Dictionary(db)
    with pytest.raises(Exception) as excinfo:
        dictionary.update("nonexistent", "en", "hi")
    assert "not found" in str(excinfo.value)


def test_search_prefix():
    db = FakeDb()
    dictionary = Dictionary(db)
    dictionary.write("hello", {"en": "greeting", "fa": "سلام", "fe": "bonjour"})
    dictionary.write("help", {"en": "assistance", "fa": "کمک", "fe": "aider"})
    dictionary.write("world", {"en": "planet", "fa": "دنیا", "fe": "monde"})
    results = dictionary.search("hel")
    assert "hello" in results
    assert "help" in results
    assert "world" not in results


def test_trie_update_on_write():
    db = FakeDb()
    dictionary = Dictionary(db)
    assert dictionary.search("any") == []
    dictionary.write("apple", {"en": "apple", "fa": "سیب", "fe": "pomme"})
    results = dictionary.search("app")
    assert "apple" in results


class FakeDbList:
    def get_whole_data(self):
        return [
            {"word": "apple", "meanings": {"en": "fruit"}},
            {"word": "banana", "meanings": {"en": "fruit"}},
            {"word": None, "meanings": {"en": "invalid"}},
        ]

    def exists(self, key: str):
        return False

    def write(self, data: dict):
        pass

    def update(self, key: str, data: dict):
        pass

    def get_or_none(self, key: str):
        return None


class FakeDbDict:
    def get_whole_data(self):
        return {
            "cherry": {"word": "cherry", "meanings": {"en": "fruit"}},
            "date": {"word": "date", "meanings": {"en": "fruit"}},
        }

    def exists(self, key: str):
        return False

    def write(self, data: dict):
        pass

    def update(self, key: str, data: dict):
        pass

    def get_or_none(self, key: str):
        return None


def test_update_trie_with_list():
    fake_db = FakeDbList()
    dictionary = Dictionary(fake_db)
    results = dictionary.search("")
    assert "apple" in results
    assert "banana" in results
    assert len(results) == 2


def test_update_trie_with_dict():
    fake_db = FakeDbDict()
    dictionary = Dictionary(fake_db)
    results = dictionary.search("")
    assert "cherry" in results
    assert "date" in results
    assert len(results) == 2
