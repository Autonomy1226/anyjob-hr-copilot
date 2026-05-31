SYSTEM_PROMPT = """You are a professional HR communication assistant. Generate personalized outreach messages for recruiting candidates on Chinese recruitment platforms.

Write messages that are:
- Professional yet warm and approachable
- Brief and to the point (suitable for instant messaging platforms)
- Personalized to the candidate's background
- Clear about the opportunity and next steps

Return ONLY valid JSON:
{
  "message": "string (the complete outreach message in Chinese)",
  "template_used": "string",
  "tokens_used": 0
}
"""

TEMPLATES = {
    "面试邀请": """Generate an interview invitation message. Include:
- Greeting by name
- Mention you've reviewed their background
- Highlight 1-2 specific strengths that match the role
- Propose interview times
- Professional closing""",

    "拒信": """Generate a polite rejection message. Include:
- Greeting by name
- Thank them for their interest
- Briefly mention the reason (role fit, not personal)
- Encourage future applications
- Professional closing""",

    "跟进": """Generate a follow-up message to re-engage a candidate. Include:
- Greeting by name
- Reference a previous interaction
- Mention new or updated opportunity details
- Ask if they're still interested
- Clear call to action""",

    "自定义": """Generate a message following the user's custom instructions. Adapt to the candidate's profile and the job context.""",
}


def build_user_prompt(
    candidate_name: str,
    candidate_summary: str,
    jd_title: str,
    jd_company: str,
    template_type: str,
    custom_instruction: str = "",
) -> str:
    template_guide = TEMPLATES.get(template_type, TEMPLATES["面试邀请"])

    if template_type == "自定义":
        template_guide += f"\n\nCustom instructions: {custom_instruction}"

    return f"""Candidate: {candidate_name}
Profile summary: {candidate_summary}
Position: {jd_title}
Company: {jd_company}

Message template type: {template_type}
Template guidance: {template_guide}

Generate the outreach message JSON:"""
