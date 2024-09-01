import httpx
import json

from .schemas import ModelRequest, ModelResponse, SketchGenRequest, STTGenRequest

from core.config import settings


# Request to AI-ML
async def get_content_aiml(req: ModelRequest):
    url = f"{settings.AI_BASE_URL}/api/v1/model"

    print(url)

    if req.image_url:
        req_json = SketchGenRequest(user_id=req.user_id, title=req.title, image_url=req.image_url)
    else:
        req_json = STTGenRequest(user_id=req.user_id, title=req.title, prompt=req.prompt)

    json_data = req_json.model_dump()

    print(json_data)

    async with httpx.AsyncClient(timeout=600.0) as cli:
        response = await cli.post(url, json=json_data)

    data = ModelResponse(**response.json())

    return data
