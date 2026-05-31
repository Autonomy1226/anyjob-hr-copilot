from pydantic import BaseModel


class RadarDimension(BaseModel):
    name: str
    score: float
    candidate_value: str
    jd_requirement: str


class MatchResult(BaseModel):
    overall_score: float
    summary: str
    radar_dimensions: list[RadarDimension]
    matched_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    recommendation: str
