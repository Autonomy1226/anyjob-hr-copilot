export interface ParseResumeRequest {
  raw_text: string
  source_site: string
}

export interface MatchCandidateRequest {
  candidate: import('./candidate').Candidate
  jd_text: string
}

export interface GenerateMessageRequest {
  candidate: import('./candidate').Candidate
  jd_title: string
  jd_company: string
  template_type: '面试邀请' | '拒信' | '跟进' | '自定义'
  custom_instruction: string
}

export interface GenerateMessageResponse {
  message: string
  template_used: string
  tokens_used: number
}

export interface DashboardStats {
  total_parsed: number
  total_matched: number
  total_messages: number
  avg_match_score: number
  daily_breakdown: Array<{
    date: string
    parsed_count: number
    matched_count: number
    message_count: number
  }>
  recent_activity: Array<{
    timestamp: string
    action: string
    candidate_name: string
    detail: string
  }>
}

export interface ApiError {
  detail: string
}
