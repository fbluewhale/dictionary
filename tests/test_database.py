import pytest
import mongomock

from db.database import DbFile, DbMongo, DbFactory, DbType

@pytest.fixture
def temp_file(tmp_path):
    """Creates a temp JSON file path for testing DbFile."""
    file_path = tmp_path / "test_db.json"
    if file_path.exists():
        file_path.unlink()
    return str(file_path)

def test_dbfile_read_empty(temp_file):
    db = DbFile(temp_file)
    assert db.read() == {}
    assert db.get_whole_data() == {}

def test_dbfile_write_and_read(temp_file):
    db = DbFile(temp_file)
    data = {"word": "hello", "meanings": {"en": "greeting"}}
    db.write(data)
    assert db.exists("hello")
    retrieved = db.get_or_none("hello")
    assert retrieved == data

def test_dbfile_update(temp_file):
    db = DbFile(temp_file)
    data = {"word": "hello", "meanings": {"en": "greeting"}}
    db.write(data)
    db.update("hello", {"meanings": {"en": "salutation"}})
    updated = db.get_or_none("hello")
    assert updated["meanings"]["en"] == "salutation"

def test_dbfile_get_whole_data(temp_file):
    db = DbFile(temp_file)
    data1 = {"word": "hello", "meanings": {"en": "greeting"}}
    data2 = {"word": "world", "meanings": {"en": "planet"}}
    db.write(data1)
    db.write(data2)
    whole = db.get_whole_data()
    assert "hello" in whole
    assert "world" in whole