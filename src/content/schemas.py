from pydantic import BaseModel, field_validator
from starlette import status
from typing import Optional

from .models import Sketch, Content
from .utils import datetime_to_str

from core.exceptions import BaseCustomException

class SketchListItem(BaseModel):
    sketch_id: int = None
    sketch_title: str = None
    sketch_url: str = None
    created_at: str = None
    updated_at: str = None

    def __init__(self, sketch: Sketch):
        super().__init__(sketch=sketch)
        self.sketch_id = sketch.sketch_id
        self.sketch_title = sketch.sketch_title
        self.sketch_url = sketch.sketch_url
        self.created_at = datetime_to_str(sketch.created_at)
        self.updated_at = datetime_to_str(sketch.updated_at)


class SketchItem(BaseModel):
    sketch_id: int = None
    sketch_title: str = None
    sketch_url: str = None
    content_id: int = None
    created_at: str = None
    updated_at: str = None

    def __init__(self, sketch: Sketch):
        super().__init__(sketch=sketch)
        self.sketch_id = sketch.sketch_id
        self.sketch_title = sketch.sketch_title
        self.sketch_url = sketch.sketch_url
        self.content_id = sketch.content_id
        self.created_at = datetime_to_str(sketch.created_at)
        self.updated_at = datetime_to_str(sketch.updated_at)


class NewSketchResponse(BaseModel):
    sketch_id: Optional[int] = None
    sketch_title: Optional[str] = None
    sketch_url: Optional[str] = None


class ContentListItem(BaseModel):
    content_id: int = None
    content_title: str = None
    content_url: str = None
    thumbnail_url: str = None
    created_at: str = None
    updated_at: str = None

    def __init__(self, content: Content):
        super().__init__(content=content)
        self.content_id = content.content_id
        self.content_title = content.content_title
        self.content_url = content.content_url
        self.thumbnail_url = content.thumbnail_url
        self.created_at = datetime_to_str(content.created_at)
        self.updated_at = datetime_to_str(content.updated_at)


class ContentItem(BaseModel):
    content_id: int = None
    content_title: str = None
    content_url: str = None
    content_bg_url: str = None
    design_url: str = None
    created_at: str = None
    updated_at: str = None

    def __init__(self, content: Content, design: str):
        super().__init__(content=content, design=design)
        self.content_id = content.content_id
        self.content_title = content.content_title
        self.content_url = content.content_url
        self.content_bg_url = content.content_bg_url
        self.design_url = design
        self.created_at = datetime_to_str(content.created_at)
        self.updated_at = datetime_to_str(content.updated_at)


class ContentRequest(BaseModel):
    sketch_id: int = None
    title: str = None

    @field_validator('sketch_id', 'title')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise BaseCustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Value required.'
            )
        return v


class STTRequest(BaseModel):
    prompt: str = None
    title: str = None

    @field_validator('prompt', 'title')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise BaseCustomException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Value required.'
            )
        return v
