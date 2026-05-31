import json
from ..models.candidate import Candidate
from ..prompts.resume_parse import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE
from .llm_client import chat_completion


async def parse_resume(raw_text: str, source_site: str = "") -> Candidate:
    """Parse raw DOM text into a structured Candidate object via DeepSeek LLM."""
    user_prompt = USER_PROMPT_TEMPLATE.format(raw_text=raw_text, source_site=source_site)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    response_text = await chat_completion(messages, temperature=0.3)
    data = json.loads(response_text)
    return Candidate.model_validate(data)
