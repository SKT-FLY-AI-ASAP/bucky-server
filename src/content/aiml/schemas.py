from pydantic import BaseModel

class ModelRequest(BaseModel):
    user_id: int
    title: str
    image_url: str = None
    prompt: str = None


class SketchGenRequest(BaseModel):
    user_id: int
    title: str
    image_url: str


class STTGenRequest(BaseModel):
    user_id: int
    title: str
    prompt: str


class ModelResponse(BaseModel):
    png_url: str = None
    bg_png_url: str = None
    stl_url: str = None
    glb_url: str = None
    mp3_url: str = None


class S3Request(BaseModel):
    object_name: str = None
    content_type: str = 'application/octet-stream'


class S3Response(BaseModel):
    url: str = None
