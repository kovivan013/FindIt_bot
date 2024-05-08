from abc import ABC
from typing import Any, Optional, Union, Dict
from datetime import datetime
from pydantic import BaseModel


class DataStructure(BaseModel):

    status: int = 200
    success: bool = False
    message: str = ""
    data: dict = {}

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


class DataModel:

    def __init__(
            self,
            data: dict
    ) -> None:
        for key, value in data.items():
            setattr(
                self, key, value
            )
            # if isinstance(value, dict):
            #     setattr(
            #         self, key, DataModel(
            #             value
            #         )
            #     )

    def as_dict(self) -> Dict[str, Any]:
        return {
            attr: value for attr, value in self.__dict__.items() if not attr.startswith('_')
        }


class OAuthStructure(BaseModel):

    id_: int = 0
    exp: int = 0