from fastapi import APIRouter, HTTPException

from ..models.message import MessageRequest
from ..services.message_generator import generate_message
from ..store.memory_store import store

router = APIRouter()


@router.post("/message/generate")
async def generate_message_endpoint(req: MessageRequest):
    try:
        result = await generate_message(req)
        store.record_message(req.candidate.name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Message generation failed: {str(e)}")
