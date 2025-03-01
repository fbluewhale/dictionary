import os
from db.database import DbFactory, DbType
from dictionary.dictionary import Dictionary
from dotenv import load_dotenv


def create_dictionary_cli() -> Dictionary:
    load_dotenv()
    file_path = os.getenv("FILE_PATH", "database.json")
    mongo_connection = os.getenv("MONGO_CONNECTION", "mongodb://localhost:27017/")
    mongo_db = os.getenv("MONGO_DB", "snap")
    mongo_collection = os.getenv("MONGO_COLLECTION", "words")

    db_type = input("Enter database type (file/mongo): ").strip().lower()
    if db_type == "file":
        db = DbFactory.create_db(DbType.FILE, file_path)
    elif db_type == "mongo":
        db = DbFactory.create_db(
            DbType.MONGO, mongo_connection, mongo_db, mongo_collection
        )
    else:
        print("Invalid database type")
        return None

    return Dictionary(db=db)


def actions_cli(dictionary: Dictionary):
    """
    Provides a menu of actions to perform on the Dictionary instance.
    """
    print("\nAvailable actions:")
    print("  get            - Retrieve a word's meaning")
    print("  add    - Define a new word")
    print("  update         - Update an existing word")
    print("  search  - Search words by prefix")
    print("  exit           - Quit the application")

    while True:
        operation = input("\nEnter operation: ").strip().lower()
        if operation == "exit":
            print("Exiting the dictionary CLI.")
            break

        if operation == "get":
            word = input("Enter the word: ").strip()
            lang = input("Enter language code: ").strip()
            try:
                result = dictionary.read(word, lang)
                print(f"Meaning for '{word}' in '{lang}': {result}")
            except Exception as e:
                print(e)

        elif operation == "add":
            word = input("Enter the word: ").strip()
            meaning_input = input(
                "Enter meaning (use fa,en,fe format for multiple languages or a single meaning): "
            ).strip()
            if "," in meaning_input:
                parts = [part.strip() for part in meaning_input.split(",")]
                if len(parts) == 3:
                    meaning = {"fa": parts[0], "en": parts[1], "fe": parts[2]}
                else:
                    print(
                        "Please provide exactly three comma-separated meanings in the order: a,b,c"
                    )
                    continue
            else:
                lang = input("Enter language code: ").strip()
                if not lang:
                    print("Language code is required when providing a single meaning.")
                    continue
                meaning = meaning_input

            try:
                success = dictionary.write(new_word=word, meanings=meaning)
                if success:
                    print(f"Word '{word}' defined!")
                else:
                    print(f"The word '{word}' already exists!")
            except Exception as e:
                print(e)

        elif operation == "update":
            word = input("Enter the word: ").strip()
            lang = input("Enter language code: ").strip()
            meaning_input = input(
                "Enter new meaning (use a,b,c format for multiple languages or a single meaning): "
            ).strip()
            if "," in meaning_input:
                parts = [part.strip() for part in meaning_input.split(",")]
                if len(parts) == 3:
                    meaning = {"fa": parts[0], "en": parts[1], "fe": parts[2]}
                else:
                    print(
                        "Please provide exactly three comma-separated meanings in the order: a,b,c"
                    )
                    continue
            else:
                if not lang:
                    print("Language code is required when providing a single meaning.")
                    continue
                meaning = meaning_input

            try:
                dictionary.update(word, lang, meaning)
                print(f"Word '{word}' updated!")
            except Exception as e:
                print(e)

        elif operation == "search":
            prefix = input("Enter prefix: ").strip()
            try:
                words = dictionary.search(prefix)
                if words:
                    print("Words starting with prefix:", words)
                else:
                    print("No words found with that prefix.")
            except Exception as e:
                print(e)

        else:
            print(
                "Invalid operation. Please choose from get, define_word, update, prefix_search, or exit."
            )
