from sqlalchemy.orm import Session
from starlette import status
from fastapi import File
from datetime import datetime

from .schemas import SketchListItem, SketchItem, NewSketchResponse, ContentListItem
from .models import Sketch, Content, Design
from .utils import add_to_s3, check_file_extension

from core.utils import decode_access_token
from core.exceptions import BaseCustomException

# Sketch List
def read_sketch_list(db: Session, authorization: str):
    # Decode access token
    user = decode_access_token(db=db, authorization=authorization)

    # Read sketch data
    sketch_list = db.query(Sketch).filter(Sketch.user_id == user.user_id).all()
    sketch_list = [SketchListItem(item) for item in sketch_list]

    return sketch_list


# Sketch item
def read_sketch_item(db: Session, authorization: str, id: int):
    # Decode access token
    user = decode_access_token(db=db, authorization=authorization)

    # Read sketch data
    sketch = db.query(Sketch).filter(Sketch.sketch_id == id).first()

    # Validation
    if not sketch:
        raise BaseCustomException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Sketch not found.'
        )
    elif sketch.user_id != user.user_id:
        raise BaseCustomException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Data access denied.'
        )

    return SketchItem(sketch=sketch)


# New sketch
def add_new_sketch(db: Session, authorization: str, title: str, file: File):
    # Decode access token
    user = decode_access_token(db=db, authorization=authorization)

    # Title validation
    if not title or not title.strip():
        raise BaseCustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Title value required.'
        )

    # File validation (file extension - png)
    if not check_file_extension(file.filename, 'png'):
        raise BaseCustomException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Wrong file extension. (png required.)'
        )

    # Add file to S3
    current_time = datetime.now().strftime('%Y%m%dT%H:%M:%S')
    url = add_to_s3(object_name=f'sketches/{user.user_id}-{title}-{current_time}.png', file=file)

    # Add sketch data
    db_sketch = Sketch(sketch_title=title,
                       sketch_url=url,
                       user_id=user.user_id)
    db.add(db_sketch)
    db.commit()
    db.refresh(db_sketch)

    print(f"New sketch {db_sketch.sketch_id} created.")

    return NewSketchResponse(sketch_id=db_sketch.sketch_id,
                             sketch_title=db_sketch.sketch_title,
                             sketch_url=db_sketch.sketch_url)


# 3D Content list (장난감 상자)
def read_content_list(db: Session, authorization: str):
    # Decode access token
    user = decode_access_token(db=db, authorization=authorization)

    # Read content data
    content_list = db.query(Content).filter(Content.user_id == user.user_id).all()
    content_list = [ContentListItem(item) for item in content_list]

    return content_list
