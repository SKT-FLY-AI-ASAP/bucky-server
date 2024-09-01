from sqlalchemy import and_
from sqlalchemy.orm import Session
from starlette import status
from fastapi import File, UploadFile
from datetime import datetime

from .schemas import SketchListItem, SketchItem, NewSketchResponse, ContentListItem, ContentItem, ContentRequest, STTRequest
from .models import Sketch, Content, Design
from .utils import add_to_s3, check_file_extension

from .aiml.service import get_content_aiml
from .aiml.schemas import ModelRequest, ModelResponse

from core.utils import decode_access_token
from core.exceptions import BaseCustomException
from core.config import settings


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
async def add_new_sketch(db: Session, authorization: str, title: str, file: UploadFile):
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
    url = await add_to_s3(object_name=f'sketches/{user.user_id}-{title}-{current_time}.png', file=file)

    print(url)

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
def read_content_list(db: Session, authorization: str, is_stt: bool = False):
    # Decode access token
    user = decode_access_token(db=db, authorization=authorization)

    # Read content data
    content_list = db.query(Content).filter(
        and_(
            Content.user_id == user.user_id,
            Content.content_type == is_stt
        )
    ).all()
    content_list = [ContentListItem(item) for item in content_list]

    return content_list


# 3D Content item (장난감 상자)
def read_content_item(db: Session, authorization: str, id: int):
    # Decode access token
    user = decode_access_token(db=db, authorization=authorization)

    # Read content data
    content = db.query(Content).filter(
        and_(
            Content.content_id == id,
            Content.is_removed == False
        )
    ).first()

    # Validation
    if not content:
        raise BaseCustomException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Content not found.'
        )
    elif content.user_id != user.user_id:
        raise BaseCustomException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Data access denied.'
        )

    # Find design data
    design = db.query(Design).filter(
        and_(
            Design.content_id == content.content_id,
            Design.is_removed == False
        )
    ).first()

    if not design:
        url = None
    else:
        url = design.design_url

    return ContentItem(content=content, design=url)


# New content
async def gen_content(db: Session, authorization: str, sketch_req: ContentRequest = None, stt_req: STTRequest = None):
    # Decode access token
    user = decode_access_token(db=db, authorization=authorization)

    # Current time
    current_time = datetime.now().strftime('%Y%m%dT%H:%M:%S')

    is_sketch = False

    # Check req type
    if stt_req is None:
        is_sketch = True
        # Read sketch data
        sketch = db.query(Sketch).filter(Sketch.sketch_id == sketch_req.sketch_id).first()

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

        req = ModelRequest(user_id=user.user_id, title=f'sketch_{current_time}', image_url=sketch.sketch_url)
        title = sketch_req.title
    else:
        req = ModelRequest(user_id=user.user_id, title=f'stt_{current_time}', prompt=stt_req.prompt)
        title = stt_req.title

    # Request ai-ml
    data = await get_content_aiml(req=req)

    # Add content to DB
    db_content = Content(
        content_title=title,
        content_type=is_sketch,
        content_url=data.glb_url,
        content_bg_url=data.bg_png_url,
        content_bgm_url=data.mp3_url,
        thumbnail_url=data.png_url,
        user_id=user.user_id
    )
    db.add(db_content)
    db.commit()
    db.refresh(db_content)

    # Add design to DB
    db_design = Design(
        design_url=data.stl_url,
        content_id=db_content.content_id
    )
    db.add(db_design)
    db.commit()
    db.refresh(db_design)

    return ContentItem(content=db_content, design=db_design.design_url)
