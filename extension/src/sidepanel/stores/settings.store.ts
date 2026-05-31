import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface SavedJd {
  id: string
  title: string
  company: string
  text: string
}

export const useSettingsStore = defineStore('settings', () => {
  const apiBaseUrl = ref('http://localhost:8000')
  const llmApiKey = ref('')
  const savedJds = ref<SavedJd[]>([])

  function addJd(jd: SavedJd) {
    savedJds.value.push(jd)
  }

  function removeJd(id: string) {
    savedJds.value = savedJds.value.filter((j) => j.id !== id)
  }

  function setApiKey(key: string) {
    llmApiKey.value = key
  }

  return { apiBaseUrl, llmApiKey, savedJds, addJd, removeJd, setApiKey }
})
