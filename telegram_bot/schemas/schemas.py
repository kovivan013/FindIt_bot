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


class OAuthStructure(BaseModel):

    id_: int = 0
    expire_at: int = 0