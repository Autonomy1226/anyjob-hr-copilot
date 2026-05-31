from collections import defaultdict
from datetime import date, datetime, timedelta
from ..models.dashboard import DashboardStats, DailyBreakdown, ActivityItem


class MemoryStore:
    def __init__(self):
        self.parse_count = 0
        self.match_count = 0
        self.message_count = 0
        self.match_scores: list[float] = []
        self.daily: dict[str, dict[str, int]] = defaultdict(lambda: {"parsed": 0, "matched": 0, "messages": 0})
        self.activities: list[ActivityItem] = []  # Most recent first

    def record_parse(self, candidate_name: str) -> None:
        today = date.today().isoformat()
        self.parse_count += 1
        self.daily[today]["parsed"] += 1
        self.activities.insert(0, ActivityItem(
            timestamp=datetime.now().isoformat(),
            action="简历解析",
            candidate_name=candidate_name,
            detail="成功解析候选人简历",
        ))
        if len(self.activities) > 50:
            self.activities.pop()

    def record_match(self, candidate_name: str, score: float) -> None:
        today = date.today().isoformat()
        self.match_count += 1
        self.match_scores.append(score)
        self.daily[today]["matched"] += 1
        self.activities.insert(0, ActivityItem(
            timestamp=datetime.now().isoformat(),
            action="人岗匹配",
            candidate_name=candidate_name,
            detail=f"匹配度评分: {score}",
        ))
        if len(self.activities) > 50:
            self.activities.pop()

    def record_message(self, candidate_name: str) -> None:
        today = date.today().isoformat()
        self.message_count += 1
        self.daily[today]["messages"] += 1
        self.activities.insert(0, ActivityItem(
            timestamp=datetime.now().isoformat(),
            action="智能消息",
            candidate_name=candidate_name,
            detail="已生成沟通消息",
        ))
        if len(self.activities) > 50:
            self.activities.pop()

    def get_stats(self, days: int = 7) -> DashboardStats:
        avg_score = sum(self.match_scores) / len(self.match_scores) if self.match_scores else 0.0

        today = date.today()
        daily_breakdown = []
        for i in range(days - 1, -1, -1):
            d = (today - timedelta(days=i)).isoformat()
            entry = self.daily.get(d, {"parsed": 0, "matched": 0, "messages": 0})
            daily_breakdown.append(DailyBreakdown(
                date=d,
                parsed_count=entry["parsed"],
                matched_count=entry["matched"],
                message_count=entry["messages"],
            ))

        return DashboardStats(
            total_parsed=self.parse_count,
            total_matched=self.match_count,
            total_messages=self.message_count,
            avg_match_score=round(avg_score, 1),
            daily_breakdown=daily_breakdown,
            recent_activity=self.activities[:20],
        )


store = MemoryStore()
