from pydantic import BaseModel

class ModelRequest(BaseModel):
    user_id: int = None
    title: str = None
    image_url: str = None
    prompt: str = None


class ModelResponse(BaseModel):
    stl_url: str = None
    glb_url: str = None
    glb_bg_url: str = None
    thumbnail_url: str = None
