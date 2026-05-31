import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Candidate } from '@/types/candidate'
import type { MatchResult } from '@/types/matching'

export const useCandidateStore = defineStore('candidate', () => {
  const rawText = ref('')
  const sourceSite = ref('')
  const parsed = ref<Candidate | null>(null)
  const matchResult = ref<MatchResult | null>(null)
  const generatedMessage = ref<string | null>(null)
  const extractionStatus = ref<'idle' | 'loading' | 'done' | 'error'>('idle')
  const matchingStatus = ref<'idle' | 'loading' | 'done' | 'error'>('idle')
  const messageStatus = ref<'idle' | 'loading' | 'done' | 'error'>('idle')
  const error = ref<string | null>(null)

  function setRawText(text: string, site: string) {
    rawText.value = text
    sourceSite.value = site
    extractionStatus.value = 'idle'
    error.value = null
  }

  function setParsed(candidate: Candidate) {
    parsed.value = candidate
    extractionStatus.value = 'done'
    error.value = null
  }

  function setExtractionError(msg: string) {
    error.value = msg
    extractionStatus.value = 'error'
  }

  function setMatchResult(result: MatchResult) {
    matchResult.value = result
    matchingStatus.value = 'done'
    error.value = null
  }

  function setMatchingError(msg: string) {
    error.value = msg
    matchingStatus.value = 'error'
  }

  function setGeneratedMessage(msg: string) {
    generatedMessage.value = msg
    messageStatus.value = 'done'
  }

  function setMessageError(msg: string) {
    error.value = msg
    messageStatus.value = 'error'
  }

  function reset() {
    rawText.value = ''
    parsed.value = null
    matchResult.value = null
    generatedMessage.value = null
    extractionStatus.value = 'idle'
    matchingStatus.value = 'idle'
    messageStatus.value = 'idle'
    error.value = null
  }

  return {
    rawText,
    sourceSite,
    parsed,
    matchResult,
    generatedMessage,
    extractionStatus,
    matchingStatus,
    messageStatus,
    error,
    setRawText,
    setParsed,
    setExtractionError,
    setMatchResult,
    setMatchingError,
    setGeneratedMessage,
    setMessageError,
    reset,
  }
})
