from typing import Any, Dict, Union
from pydantic import BaseModel

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

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



