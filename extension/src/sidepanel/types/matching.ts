export interface RadarDimension {
  name: string
  score: number
  candidate_value: string
  jd_requirement: string
}

export interface SkillGap {
  skill: string
  required: boolean
  candidate_has: boolean
  level: string
}

export interface MatchResult {
  overall_score: number
  summary: string
  radar_dimensions: RadarDimension[]
  matched_skills: string[]
  missing_skills: string[]
  strengths: string[]
  weaknesses: string[]
  recommendation: string
}
