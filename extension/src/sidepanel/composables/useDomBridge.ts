// Type-safe message bridge between side panel and content script

interface ExtractResponse {
  rawText: string
  sourceSite: string
  url: string
}

export function useDomBridge() {
  async function getExtractedText(): Promise<ExtractResponse> {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true })
    if (!tab?.id) {
      throw new Error('No active tab found')
    }

    return new Promise<ExtractResponse>((resolve, reject) => {
      chrome.tabs.sendMessage(tab.id!, { type: 'EXTRACT_DOM' }, (response) => {
        if (chrome.runtime.lastError) {
          reject(new Error(chrome.runtime.lastError.message))
          return
        }
        if (!response?.rawText) {
          reject(new Error('No content extracted from page'))
          return
        }
        resolve(response as ExtractResponse)
      })
    })
  }

  return { getExtractedText }
}
