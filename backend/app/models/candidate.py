from pydantic import BaseModel


class Education(BaseModel):
    school: str = ""
    degree: str = ""
    major: str = ""
    graduation_year: int | None = None


class WorkExperience(BaseModel):
    company: str = ""
    title: str = ""
    duration_months: int = 0
    description: str = ""
    skills_used: list[str] = []


class Candidate(BaseModel):
    name: str = ""
    gender: str = ""
    age: int = 0
    years_of_experience: int = 0
    current_title: str = ""
    current_company: str = ""
    education: list[Education] = []
    work_experience: list[WorkExperience] = []
    skills: list[str] = []
    languages: list[str] = []
    salary_expectation: str = ""
    location: str = ""
    summary: str = ""
    source_raw_text: str = ""
