import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface HistoryEntry {
  id: string
  candidateName: string
  sourceSite: string
  timestamp: number
  matchScore: number | null
}

export const useHistoryStore = defineStore('history', () => {
  const recentCandidates = ref<HistoryEntry[]>([])
  const recentMessages = ref<Array<{ message: string; timestamp: number }>>([])

  function addCandidate(entry: HistoryEntry) {
    recentCandidates.value.unshift(entry)
    if (recentCandidates.value.length > 50) {
      recentCandidates.value.length = 50
    }
  }

  function addMessage(message: string) {
    recentMessages.value.unshift({ message, timestamp: Date.now() })
    if (recentMessages.value.length > 50) {
      recentMessages.value.length = 50
    }
  }

  return { recentCandidates, recentMessages, addCandidate, addMessage }
})
