// Content Script Entry — Detects candidate profile pages, extracts DOM text, injects trigger button

import { DomExtractor } from './dom-extractor'
import { getAdapterForSite } from './site-adapters'
import { injectSidebarTrigger } from './sidebar-injector'

const SCRIPT_ID = 'anyjob-hr-copilot'

function isCandidatePage(): boolean {
  const hostname = window.location.hostname
  const pathname = window.location.pathname

  if (hostname.includes('zhipin.com')) {
    return pathname.includes('/geek/') || pathname.includes('/resume/')
  }
  if (hostname.includes('liepin.com')) {
    return pathname.includes('/resume/') || pathname.includes('/profile/')
  }
  if (hostname.includes('zhaopin.com')) {
    return pathname.includes('/resume/') || pathname.includes('/jobseeker/')
  }
  if (hostname.includes('localhost') || hostname.includes('127.0.0.1')) {
    return true
  }
  return false
}

function init(): void {
  if (document.getElementById(SCRIPT_ID)) return // Already injected

  if (!isCandidatePage()) return

  const adapter = getAdapterForSite(window.location.hostname)
  if (!adapter) return

  const extractor = new DomExtractor(adapter)
  const rawText = extractor.extract()

  if (!rawText || rawText.length < 50) return // Not enough content

  injectSidebarTrigger(rawText)
}

// Listen for re-extraction requests from side panel
chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type === 'EXTRACT_DOM') {
    const adapter = getAdapterForSite(window.location.hostname)
    if (adapter) {
      const extractor = new DomExtractor(adapter)
      const rawText = extractor.extract()
      sendResponse({
        rawText,
        sourceSite: adapter.name,
        url: window.location.href,
      })
    } else {
      sendResponse({ rawText: '', sourceSite: '', url: window.location.href })
    }
    return true
  }
})

// Run on page load
if (document.readyState === 'complete') {
  init()
} else {
  window.addEventListener('load', init)
}
