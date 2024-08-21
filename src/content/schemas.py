from pydantic import BaseModel
from typing import List

from .models import Sketch
from .utils import datetime_to_str

class SketchItem(BaseModel):
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

class SketchListResponse(BaseModel):
    sketch_list: List[SketchItem] = []
