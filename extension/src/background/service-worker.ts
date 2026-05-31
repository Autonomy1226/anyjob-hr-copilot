// Background Service Worker — Manages side panel lifecycle and message relay

interface SidePanelMessage {
  type: 'OPEN_SIDE_PANEL'
  tabId?: number
}

// Listen for action button click
chrome.action.onClicked.addListener((tab) => {
  if (tab.id) {
    chrome.sidePanel.open({ tabId: tab.id })
  }
})

// Listen for messages from content scripts to open side panel
chrome.runtime.onMessage.addListener(
  (message: SidePanelMessage, sender, sendResponse) => {
    if (message.type === 'OPEN_SIDE_PANEL') {
      const tabId = message.tabId || sender.tab?.id
      if (tabId) {
        chrome.sidePanel.open({ tabId })
      }
    }
    sendResponse({ ok: true })
    return true
  }
)
