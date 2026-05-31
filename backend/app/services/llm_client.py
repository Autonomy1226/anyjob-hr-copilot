import json
from openai import AsyncOpenAI
from ..config import settings

_client: AsyncOpenAI | None = None


def get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        _client = AsyncOpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )
    return _client


def _is_mock() -> bool:
    return settings.deepseek_api_key.startswith("sk-test-")


MOCK_RESUME = json.dumps({
    "name": "张小明",
    "gender": "男",
    "age": 28,
    "years_of_experience": 5,
    "current_title": "高级前端开发工程师",
    "current_company": "字节跳动",
    "education": [
        {"school": "上海交通大学", "degree": "本科", "major": "计算机科学与技术", "graduation_year": 2019}
    ],
    "work_experience": [
        {
            "company": "字节跳动",
            "title": "高级前端开发工程师",
            "duration_months": 36,
            "description": "负责抖音电商平台前端架构设计，使用 Vue3+TypeScript 开发核心业务模块",
            "skills_used": ["Vue3", "TypeScript", "Webpack", "Node.js"]
        },
        {
            "company": "阿里巴巴",
            "title": "前端开发工程师",
            "duration_months": 24,
            "description": "参与淘宝商家后台系统开发，负责订单管理、商品管理等模块",
            "skills_used": ["React", "JavaScript", "Redux", "Ant Design"]
        }
    ],
    "skills": ["Vue3", "TypeScript", "React", "JavaScript", "Node.js", "CSS3", "HTML5", "Git", "Webpack", "Chrome Extension"],
    "languages": ["中文", "英语"],
    "salary_expectation": "30K-40K",
    "location": "上海",
    "summary": "5年前端开发经验，精通 Vue3 和 React，有大型电商平台开发经验，善于前端工程化和性能优化"
})

MOCK_MATCH = json.dumps({
    "overall_score": 82,
    "summary": "候选人张小明具有5年前端开发经验，技术栈与岗位要求高度匹配。有字节跳动和阿里巴巴的工作背景，项目经验丰富，尤其在 Vue3/TypeScript 方面能力突出。建议推进面试流程。",
    "radar_dimensions": [
        {"name": "技术技能", "score": 90, "candidate_value": "Vue3, React, TypeScript, Node.js", "jd_requirement": "Vue3/React, TypeScript"},
        {"name": "工作经验", "score": 85, "candidate_value": "5年，字节跳动+阿里", "jd_requirement": "3年以上"},
        {"name": "学历背景", "score": 80, "candidate_value": "上海交大本科", "jd_requirement": "本科及以上"},
        {"name": "薪资匹配", "score": 75, "candidate_value": "30K-40K", "jd_requirement": "25K-40K"},
        {"name": "综合素养", "score": 80, "candidate_value": "大厂背景，沟通能力好", "jd_requirement": "团队协作能力"}
    ],
    "matched_skills": ["Vue3", "TypeScript", "React", "JavaScript", "Chrome Extension"],
    "missing_skills": ["Python", "Docker"],
    "strengths": ["前端技术栈全面，覆盖 Vue3 和 React", "有大厂工作经验，项目背景扎实", "浏览器插件开发经验是加分项"],
    "weaknesses": ["后端技术储备相对薄弱", "团队管理经验不足"],
    "recommendation": "强烈推荐"
})

MOCK_MESSAGE = json.dumps({
    "message": "张小明确认好！\n\n我是 AnyJob 平台的 HR，仔细看了你的简历，你在字节跳动和阿里巴巴的前端开发经验与我们的高级前端岗非常匹配，尤其是 Vue3 和 TypeScript 的技术栈。\n\n我们正在寻找一位有浏览器插件开发经验的前端工程师，你的 Chrome Extension 经验正好是加分项。\n\n方便约个时间聊聊吗？本周三或周四下午都可以，线上视频面试大约30分钟。期待你的回复！",
    "template_used": "面试邀请",
    "tokens_used": 0
})


async def chat_completion(messages: list[dict], temperature: float = 0.3, max_retries: int = 2) -> str:
    """Call DeepSeek chat completion with retry logic. Uses mock data when API key is test key."""

    if _is_mock():
        # Determine which mock response to return based on the system prompt
        system_msg = messages[0]["content"] if messages else ""

        if "resume parsing" in system_msg.lower() or "structured candidate" in system_msg.lower():
            return MOCK_RESUME
        elif "recruitment evaluator" in system_msg.lower() or "evaluate the candidate" in system_msg.lower():
            return MOCK_MATCH
        elif "communication assistant" in system_msg.lower() or "outreach message" in system_msg.lower():
            return MOCK_MESSAGE
        else:
            return MOCK_RESUME

    client = get_client()
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            response = await client.chat.completions.create(
                model=settings.deepseek_model,
                messages=messages,
                temperature=temperature,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content
            if content:
                json.loads(content)
                return content
        except (json.JSONDecodeError, Exception) as e:
            last_error = e
            if attempt < max_retries:
                messages.append({
                    "role": "user",
                    "content": "Your previous response was not valid JSON. Please retry with valid JSON only.",
                })
                continue

    raise RuntimeError(f"LLM call failed after {max_retries} retries: {last_error}")
