from starlette import status
from schemas.base import DataStructure
from fastapi import HTTPException
from fastapi import exceptions


UnautorizedException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unautorized"
)

ItemExists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Item already exists"
)

ItemNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Item not fount"
)

InvalidInputData = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Invalid input data"
)

NoAccess = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="No access to content"
)

ValidationException = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Validation error"
)