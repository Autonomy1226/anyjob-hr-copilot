from fastapi import APIRouter, Query

from ..store.memory_store import store

router = APIRouter()


@router.get("/dashboard/stats")
async def get_dashboard_stats(days: int = Query(7, ge=1, le=30)):
    return store.get_stats(days)
