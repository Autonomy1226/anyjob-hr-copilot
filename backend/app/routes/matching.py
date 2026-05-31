from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..models.candidate import Candidate
from ..services.matcher import match_candidate
from ..store.memory_store import store

router = APIRouter()


class MatchRequest(BaseModel):
    candidate: Candidate
    jd_text: str


@router.post("/matching/score")
async def match_candidate_endpoint(req: MatchRequest):
    if not req.jd_text.strip():
        raise HTTPException(status_code=400, detail="jd_text is required")

    try:
        result = await match_candidate(req.candidate, req.jd_text)
        store.record_match(req.candidate.name, result.overall_score)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Matching failed: {str(e)}")
