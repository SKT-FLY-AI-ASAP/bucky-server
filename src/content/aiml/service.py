import httpx

from .schemas import ModelRequest, ModelResponse

from core.config import settings


# Request to AI-ML
async def get_content_aiml(req: ModelRequest):
    url = f"{settings.AI_BASE_URL}/api/v1/model"

    async with httpx.AsyncClient() as cli:
        response = await cli.post(url, json=req)

    data = ModelResponse(**response.json())

    return data
