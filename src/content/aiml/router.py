from fastapi import APIRouter, Depends, Header, Form, File, UploadFile, Body
from starlette import status

from sqlalchemy.orm import Session

from core.database import get_db
from core.schemas import ResponseDto, DataResponseDto

from .schemas import S3Request, S3Response
from ..utils import add_to_s3

# Router
router = APIRouter(
    prefix="/api/v1/s3",
)


# Add file to S3
@router.post("", response_model=DataResponseDto[S3Response], status_code=status.HTTP_201_CREATED)
async def add_file_to_s3(file: UploadFile = File(...),
                         object_name: str = Form(...),
                         content_type: str = Form(...)):
    print(object_name, content_type)

    url = await add_to_s3(object_name=object_name, file=file, content_type=content_type)
    print(url)
    data = S3Response(url=url)

    return DataResponseDto(data=data)
