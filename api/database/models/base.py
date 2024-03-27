from typing import Any, Dict

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