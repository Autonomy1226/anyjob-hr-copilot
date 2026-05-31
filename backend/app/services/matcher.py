import json
from ..models.candidate import Candidate
from ..models.matching import MatchResult
from ..prompts.matching import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from .llm_client import chat_completion


def _format_candidate(c: Candidate) -> str:
    parts = [
        f"Name: {c.name}",
        f"Current: {c.current_title} at {c.current_company}",
        f"Experience: {c.years_of_experience} years",
        f"Location: {c.location}",
        f"Salary Expectation: {c.salary_expectation}",
        f"Skills: {', '.join(c.skills)}",
        f"Languages: {', '.join(c.languages)}",
    ]

    if c.education:
        edu_str = "; ".join(
            f"{e.degree} in {e.major} from {e.school}" + (f" ({e.graduation_year})" if e.graduation_year else "")
            for e in c.education
        )
        parts.append(f"Education: {edu_str}")

    if c.work_experience:
        exp_str = "; ".join(
            f"{w.title} at {w.company} ({w.duration_months // 12}y)" for w in c.work_experience[:5]
        )
        parts.append(f"Work History: {exp_str}")

    if c.summary:
        parts.append(f"Summary: {c.summary}")

    return "\n".join(parts)


async def match_candidate(candidate: Candidate, jd_text: str) -> MatchResult:
    """Evaluate candidate against a job description via DeepSeek LLM."""
    profile_text = _format_candidate(candidate)
    user_prompt = USER_PROMPT_TEMPLATE.format(profile_text=profile_text, jd_text=jd_text)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    response_text = await chat_completion(messages, temperature=0.3)
    data = json.loads(response_text)
    return MatchResult.model_validate(data)
