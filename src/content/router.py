from fastapi import APIRouter, Depends, Header
from starlette import status

from sqlalchemy.orm import Session

from core.database import get_db
from core.schemas import ResponseDto, DataResponseDto

from .service import read_sketch_list
from .schemas import SketchListResponse

# Router
router = APIRouter(
    prefix="/api/v1/doc",
)

# Read sketch list
@router.get("/2d/list", response_model=DataResponseDto[SketchListResponse], status_code=status.HTTP_200_OK)
def get_sketch_list(db: Session = Depends(get_db), Authorization: str = Header(default=None)):
    data = read_sketch_list(db=db, authorization=Authorization)

    return DataResponseDto(data=data, message='OK.')


# @router.post("/2d", response_model=DataResponseDto[NewSketchResponse], status_code=status.HTTP_201_CREATED)
# async def add_new_sketch(
#     title: str = Form(...),
#     file: UploadFile = File(...)
# ):
