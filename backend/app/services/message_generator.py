import json
from ..models.message import MessageRequest, MessageResponse
from ..prompts.message import SYSTEM_PROMPT, build_user_prompt
from .llm_client import chat_completion


async def generate_message(req: MessageRequest) -> MessageResponse:
    """Generate a personalized outreach message via DeepSeek LLM."""
    user_prompt = build_user_prompt(
        candidate_name=req.candidate.name,
        candidate_summary=req.candidate.summary or f"{req.candidate.current_title} at {req.candidate.current_company}",
        jd_title=req.jd_title,
        jd_company=req.jd_company,
        template_type=req.template_type,
        custom_instruction=req.custom_instruction,
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    response_text = await chat_completion(messages, temperature=0.7)
    data = json.loads(response_text)
    return MessageResponse.model_validate(data)
