from fastapi import APIRouter, Depends, Header, Form, File, UploadFile
from starlette import status

from sqlalchemy.orm import Session

from core.database import get_db
from core.schemas import ResponseDto, DataResponseDto

from .service import read_sketch_list, read_sketch_item, add_new_sketch, read_content_list, read_content_item
from .schemas import SketchItem, NewSketchResponse, ContentItem

# Router
router = APIRouter(
    prefix="/api/v1/doc",
)

# Read sketch list
@router.get("/2d/list", response_model=DataResponseDto[list], status_code=status.HTTP_200_OK)
def get_sketch_list(db: Session = Depends(get_db), Authorization: str = Header(default=None)):
    data = read_sketch_list(db=db, authorization=Authorization)

    return DataResponseDto(data=data)


# Read sketch item
@router.get("/2d/{id}", response_model=DataResponseDto[SketchItem], status_code=status.HTTP_200_OK)
def get_sketch_item(db: Session = Depends(get_db), Authorization: str = Header(default=None), id: int = 0):
    data = read_sketch_item(db=db, authorization=Authorization, id=id)

    return DataResponseDto(data=data)


# Add new sketch
@router.post("/2d", response_model=DataResponseDto[NewSketchResponse], status_code=status.HTTP_201_CREATED)
def post_new_sketch(db: Session = Depends(get_db), Authorization: str = Header(default=None),
                    title: str = Form(...), file: UploadFile = File(...)):
    data = add_new_sketch(db=db, authorization=Authorization, title=title, file=file)

    return DataResponseDto(data=data)


# 3D Content list (장난감 상자)
@router.get("/3d/list", response_model=DataResponseDto[list], status_code=status.HTTP_200_OK)
def get_content_list(db: Session = Depends(get_db), Authorization: str = Header(default=None)):
    data = read_content_list(db=db, authorization=Authorization)

    return DataResponseDto(data=data)


# 3D Content item (장난감 상자)
@router.get("/3d/{id}", response_model=DataResponseDto[ContentItem], status_code=status.HTTP_200_OK)
def get_content_item(db: Session = Depends(get_db), Authorization: str = Header(default=None), id: int = 0):
    data = read_content_item(db=db, authorization=Authorization, id=id)

    return DataResponseDto(data=data)
