from sqlalchemy.orm import Session

from .schemas import SketchItem, SketchListResponse
from .models import Sketch

from core.utils import decode_access_token

# Sketch List
def read_sketch_list(db: Session, authorization: str):
    # Decode access token
    user = decode_access_token(db=db, authorization=authorization)

    # Read sketch data
    sketch_list = db.query(Sketch).filter(Sketch.user_id == user.user_id).all()
    sketch_list = [SketchItem(item) for item in sketch_list]

    return SketchListResponse(sketch_list=sketch_list)
