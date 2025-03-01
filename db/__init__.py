from enum import Enum
from abc import ABC, abstractmethod


class DbInterface(ABC):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, data: dict):
        pass

    @abstractmethod
    def exists(self, key: str):
        pass

    @abstractmethod
    def get_or_none(self, key: str):
        pass

    @abstractmethod
    def update(self, key: str, data: dict):
        pass


class DbType(Enum):
    FILE = "file"
    MONGO = "mongo"
