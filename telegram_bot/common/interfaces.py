from pydantic import BaseModel
from typing import Dict, Any, Union, TypeVar


class DataModel:

    def __init__(
            self,
            data: dict
    ) -> None:
        for key, value in data.items():
            setattr(
                self, key, value
            )
            if isinstance(value, dict):
                setattr(
                    self, key, DataModel(
                        value
                    )
                )

    def __bool__(self):
        return bool(
            vars(self)
        )

    def __repr__(self):
        params = ', '.join(
            f'{attr}: {value!r}'
            for attr, value in self.__dict__.items()
            if not attr.startswith('_')
        )

        return f"{{{params}}}"

    def as_dict(self) -> Dict[str, Any]:
        return {
            attr: value for attr, value in self.__dict__.items() if not attr.startswith('_')
        }

    def model_dump(self) -> Dict[str, Any]:
        data: dict = {}

        for attr, value in self.__dict__.items():
            if not attr.startswith("_"):
                if isinstance(value, dict):
                    data.update({
                        attr: DataModel(
                            value
                        ).model_dump()
                    })
                elif isinstance(value, DataModel):
                    data.update({
                        attr: value.model_dump()
                    })
                else:
                    data.update({
                        attr: value
                    })

        return data


class DataStructure(BaseModel):

    status: int = 200
    success: bool = False
    message: str = ""
    data: Union[
        Dict[Any, Any],
        Any
    ] = {}

    @property
    def _success(self) -> bool:
        return self.success

    @property
    def _status(self) -> int:
        return self.status

    @_status.setter
    def _status(self, value: int) -> None:
        self.status = value
        if value in range(200, 300):
            self.success = True

    @_success.getter
    def _success(self) -> bool:
        return self.status in range(200, 300) and self.success


class OAuthStructure(BaseModel):

    id_: int = 0
    exp: int = 0