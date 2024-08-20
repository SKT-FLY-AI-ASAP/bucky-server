from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

# Generic type
T = TypeVar('T')

class ResponseDto(BaseModel):
    message: str

class DataResponseDto(BaseModel, Generic[T]):
    data: Optional[T]
    message: str

    class Config:
        from_attributes = True
