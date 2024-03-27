from starlette import status
from fastapi import HTTPException


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