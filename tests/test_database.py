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


@pytest.fixture(autouse=True)
def patch_mongo(monkeypatch):
    monkeypatch.setattr("db.database.MongoClient", mongomock.MongoClient)


@pytest.fixture
def mongo_db(monkeypatch):
    """
    Creates a mock db For mongodb
    """
    db = DbMongo("mongodb://localhost:27017/", "testdb", "testcollection")
    db.collection.delete_many({})
    return db


def test_dbmongo_initially_empty(mongo_db):
    data = mongo_db.get_whole_data()
    assert data == []


def test_dbmongo_write_and_read(mongo_db):
    data = {"word": "hello", "meanings": {"en": "greeting"}}
    mongo_db.write(data)
    assert mongo_db.exists("hello")
    retrieved = mongo_db.get_or_none("hello")
    assert retrieved == data


def test_dbmongo_update(mongo_db):
    data = {"word": "hello", "meanings": {"en": "greeting"}}
    mongo_db.write(data)
    # Update the meaning.
    mongo_db.update("hello", {"meanings": {"en": "salutation"}})
    updated = mongo_db.get_or_none("hello")
    assert updated["meanings"]["en"] == "salutation"


def test_dbmongo_get_whole_data(mongo_db):
    data1 = {"word": "hello", "meanings": {"en": "greeting"}}
    data2 = {"word": "world", "meanings": {"en": "planet"}}
    mongo_db.write(data1)
    mongo_db.write(data2)
    whole = mongo_db.get_whole_data()
    words = [doc["word"] for doc in whole]
    assert "hello" in words
    assert "world" in words


def test_dbmongo_read_db(mongo_db):
    data1 = {"word": "hello", "meanings": {"en": "greeting"}}
    data2 = {"word": "world", "meanings": {"en": "planet"}}
    mongo_db.write(data1)
    mongo_db.write(data2)
    db_data = mongo_db.read()
    assert data1 in db_data
    assert data2 in db_data


def test_dbfactory_file(tmp_path):
    file_path = tmp_path / "test_db.json"
    db = DbFactory.create_db(DbType.FILE, str(file_path))
    assert isinstance(db, DbFile)


def test_dbfactory_mongo(monkeypatch):
    db = DbFactory.create_db(
        DbType.MONGO, "mongodb://localhost:27017/", "testdb", "testcollection"
    )
    from db.database import DbMongo

    assert isinstance(db, DbMongo)


def test_dbfactory_mongo_invalid():
    with pytest.raises(ValueError) as excinfo:
        DbFactory.create_db(DbType.MONGO, "mongodb://localhost:27017/", None, None)
    assert "MongoDB requires both a database name and collection name." in str(
        excinfo.value
    )


def test_dbfactory_invalid():
    with pytest.raises(ValueError):
        DbFactory.create_db("invalid", "dummy")
