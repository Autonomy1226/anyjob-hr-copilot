export interface Education {
  school: string
  degree: string
  major: string
  graduation_year: number | null
}

export interface WorkExperience {
  company: string
  title: string
  duration_months: number
  description: string
  skills_used: string[]
}

export interface Candidate {
  name: string
  gender: string
  age: number
  years_of_experience: number
  current_title: string
  current_company: string
  education: Education[]
  work_experience: WorkExperience[]
  skills: string[]
  languages: string[]
  salary_expectation: string
  location: string
  summary: string
  source_raw_text: string
}
