from typing import Any, Dict, Union
from schemas.base import DataModel
from pydantic import BaseModel
from string import ascii_uppercase

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls) -> str:
        start_index = -1
        separated_words = []

        for i, v in enumerate(cls.__name__):
            if v in ascii_uppercase:
                if start_index >= 0 and i > start_index:
                    separated_words.append(
                        cls.__name__[start_index:i].lower()
                    )
                start_index = i
        separated_words.append(cls.__name__[start_index:].lower())

        return "_".join(
            separated_words
        )

    def __repr__(self) -> str:
        params = ', '.join(
            f'{attr}={value!r}'
            for attr, value in self.__dict__.items()
            if not attr.startswith('_')
        )
        return f'{type(self).__name__}({params})'

    def as_dict(self) -> Dict[str, Any]:
        return {
            attr: value for attr, value in self.__dict__.items() if not attr.startswith('_')
        }

    def as_data_model(self) -> Union[DataModel]:
        return DataModel(
            self.as_dict()
        )

    def validate(self, obj: dict):
        data = self.as_dict()
        for i, v in obj.items():
            if i in data:
                setattr(
                    self,
                    i,
                    v
                )

        return self



