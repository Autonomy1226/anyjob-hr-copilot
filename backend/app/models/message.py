from pydantic import BaseModel
from .candidate import Candidate


class MessageRequest(BaseModel):
    candidate: Candidate
    jd_title: str = ""
    jd_company: str = ""
    template_type: str = "面试邀请"
    custom_instruction: str = ""


class MessageResponse(BaseModel):
    message: str
    template_used: str
    tokens_used: int
