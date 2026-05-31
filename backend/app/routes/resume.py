from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.resume_parser import parse_resume
from ..store.memory_store import store

router = APIRouter()


class ParseRequest(BaseModel):
    raw_text: str
    source_site: str = ""


@router.post("/resume/parse")
async def parse_resume_endpoint(req: ParseRequest):
    if not req.raw_text.strip():
        raise HTTPException(status_code=400, detail="raw_text is required")

    try:
        candidate = await parse_resume(req.raw_text, req.source_site)
        candidate.source_raw_text = req.raw_text
        store.record_parse(candidate.name)
        return candidate
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resume parsing failed: {str(e)}")
