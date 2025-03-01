# Dictionary CLI Project
This project features a command-line dictionary application that enables users to add, update, retrieve, and search for words along with their meanings. It supports multiple storage backends, including a file-based JSON database and MongoDB. Additionally, the application incorporates a Trie data structure for fast and efficient prefix-based searches.

## Features
- Define Word: Add new words along with their definitions, supporting multiple languages.
- Update Words: Modify existing word definitions.
- Retrieve Word: Fetch the meaning of a word in a specified language.
-  Prefix Search: Quickly find words that start with a particular prefix using a Trie.
-  Multiple Storage Options: Choose between a file-based JSON database and MongoDB.
-  Environment Configuration: Easily configure file paths and MongoDB connection details through a .env file.


## Prerequisites
- Python 3.12

## Installation
Clone the repository:
  ```bash
   git https://github.com/fbluewhale/dictionary.git
   cd dictionary
   ```
(Optional) Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate 
```
## Install required packages:
```
pip install -r requirements.txt
```

## Configuration
Create a .env file in the project root with the following content:

```
FILE_PATH=database.json

MONGO_CONNECTION=mongodb://localhost:27017/

MONGO_DB=snap

MONGO_COLLECTION=words
```

Adjust these values as needed for your environment.

## Usage
Run the main CLI application:
```
python main.py
```