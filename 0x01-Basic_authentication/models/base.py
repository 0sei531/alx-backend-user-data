#!/usr/bin/env python3
""" Base module
"""
from datetime import datetime
from typing import TypeVar, List, Dict, Optional, Iterable
from os import path
import json
import uuid

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATA: Dict[str, Dict[str, 'Base']] = {}


class Base:
    """ Base class for models """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a Base instance """
        s_class = str(self.__class__.__name__)
        if DATA.get(s_class) is None:
            DATA[s_class] = {}

        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.created_at = self._str_to_datetime(kwargs.get('created_at')) or datetime.utcnow()
        self.updated_at = self._str_to_datetime(kwargs.get('updated_at')) or datetime.utcnow()

    def __eq__(self, other: TypeVar('Base')) -> bool:
        """ Check equality based on ID """
        if not isinstance(other, Base):
            return False
        return self.id == other.id

    def to_json(self, for_serialization: bool = False) -> dict:
        """ Convert the object to a JSON dictionary """
        result = {}
        for key, value in self.__dict__.items():
            if not for_serialization and key.startswith('_'):
                continue
            if isinstance(value, datetime):
                result[key] = value.strftime(TIMESTAMP_FORMAT)
            else:
                result[key] = value
        return result

    @classmethod
    def _str_to_datetime(cls, date_str: Optional[str]) -> Optional[datetime]:
        """ Convert a string to a datetime object """
        if date_str:
            return datetime.strptime(date_str, TIMESTAMP_FORMAT)
        return None

    @classmethod
    def load_from_file(cls) -> None:
        """ Load all objects from a JSON file """
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        DATA[s_class] = {}
        if not path.exists(file_path):
            return

        with open(file_path, 'r') as file:
            objs_json = json.load(file)
            for obj_id, obj_json in objs_json.items():
                DATA[s_class][obj_id] = cls(**obj_json)

    @classmethod
    def save_to_file(cls) -> None:
        """ Save all objects to a JSON file """
        s_class = cls.__name__
        file_path = f".db_{s_class}.json"
        objs_json = {obj_id: obj.to_json(True) for obj_id, obj in DATA[s_class].items()}

        with open(file_path, 'w') as file:
            json.dump(objs_json, file)

    def save(self) -> None:
        """ Save the current object """
        s_class = self.__class__.__name__
        self.updated_at = datetime.utcnow()
        DATA[s_class][self.id] = self
        self.__class__.save_to_file()

    def remove(self) -> None:
        """ Remove the current object """
        s_class = self.__class__.__name__
        if DATA[s_class].get(self.id):
            del DATA[s_class][self.id]
            self.__class__.save_to_file()

    @classmethod
    def count(cls) -> int:
        """ Count all objects """
        s_class = cls.__name__
        return len(DATA[s_class])

    @classmethod
    def all(cls) -> Iterable[TypeVar('Base')]:
        """ Return all objects """
        return cls.search()

    @classmethod
    def get(cls, id: str) -> Optional[TypeVar('Base')]:
        """ Return one object by ID """
        s_class = cls.__name__
        return DATA[s_class].get(id)

    @classmethod
    def search(cls, attributes: dict = {}) -> List[TypeVar('Base')]:
        """ Search all objects with matching attributes """
        s_class = cls.__name__

        def _search(obj: 'Base') -> bool:
            if not attributes:
                return True
            for k, v in attributes.items():
                if getattr(obj, k) != v:
                    return False
            return True

        return list(filter(_search, DATA[s_class].values()))
