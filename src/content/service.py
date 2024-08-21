from sqlalchemy.orm import Session
from starlette import status

from .schemas import SketchListItem, SketchItem
from .models import Sketch

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
