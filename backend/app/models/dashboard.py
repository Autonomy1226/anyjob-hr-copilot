from pydantic import BaseModel


class DailyBreakdown(BaseModel):
    date: str
    parsed_count: int
    matched_count: int
    message_count: int


class ActivityItem(BaseModel):
    timestamp: str
    action: str
    candidate_name: str
    detail: str


class DashboardStats(BaseModel):
    total_parsed: int
    total_matched: int
    total_messages: int
    avg_match_score: float
    daily_breakdown: list[DailyBreakdown]
    recent_activity: list[ActivityItem]
