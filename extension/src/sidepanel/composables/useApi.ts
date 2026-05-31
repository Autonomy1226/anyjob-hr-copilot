import { useSettingsStore } from '@/stores/settings.store'
import type { Candidate } from '@/types/candidate'
import type { MatchResult } from '@/types/matching'
import type {
  ParseResumeRequest,
  GenerateMessageRequest,
  GenerateMessageResponse,
  DashboardStats,
} from '@/types/api'

function baseUrl(): string {
  return useSettingsStore().apiBaseUrl
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${baseUrl()}${path}`
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail || `HTTP ${res.status}`)
  }

  return res.json()
}

export function useApi() {
  async function parseResume(payload: ParseResumeRequest): Promise<Candidate> {
    return request<Candidate>('/api/resume/parse', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  }

  async function matchCandidate(candidate: Candidate, jdText: string): Promise<MatchResult> {
    return request<MatchResult>('/api/matching/score', {
      method: 'POST',
      body: JSON.stringify({ candidate, jd_text: jdText }),
    })
  }

  async function generateMessage(
    candidate: Candidate,
    jdTitle: string,
    jdCompany: string,
    templateType: GenerateMessageRequest['template_type'],
    customInstruction = ''
  ): Promise<GenerateMessageResponse> {
    return request<GenerateMessageResponse>('/api/message/generate', {
      method: 'POST',
      body: JSON.stringify({
        candidate,
        jd_title: jdTitle,
        jd_company: jdCompany,
        template_type: templateType,
        custom_instruction: customInstruction,
      }),
    })
  }

  async function getDashboardStats(days = 7): Promise<DashboardStats> {
    return request<DashboardStats>(`/api/dashboard/stats?days=${days}`)
  }

  async function healthCheck(): Promise<{ status: string; model: string }> {
    return request('/api/health')
  }

  return { parseResume, matchCandidate, generateMessage, getDashboardStats, healthCheck }
}
