// Injects a floating trigger button into recruitment platform pages
// Uses shadow DOM for CSS isolation from the host page

const INJECTION_ID = 'anyjob-hr-copilot'

export function injectSidebarTrigger(rawText: string): void {
  if (document.getElementById(INJECTION_ID)) return

  // Create shadow DOM container for style isolation
  const container = document.createElement('div')
  container.id = INJECTION_ID
  document.body.appendChild(container)

  const shadow = container.attachShadow({ mode: 'open' })

  const style = document.createElement('style')
  style.textContent = `
    .aj-trigger {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 999999;
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 12px 20px;
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      color: #fff;
      border: none;
      border-radius: 28px;
      font-size: 14px;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4);
      transition: all 0.25s ease;
      user-select: none;
    }
    .aj-trigger:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 24px rgba(99, 102, 241, 0.55);
      background: linear-gradient(135deg, #4f46e5, #7c3aed);
    }
    .aj-trigger:active {
      transform: translateY(0);
    }
    .aj-icon {
      font-size: 18px;
    }
  `

  const button = document.createElement('button')
  button.className = 'aj-trigger'
  button.innerHTML = `
    <span class="aj-icon">&#x1F916;</span>
    <span>AI 解析</span>
  `
  button.addEventListener('click', () => {
    chrome.runtime.sendMessage({ type: 'OPEN_SIDE_PANEL' })
  })

  shadow.appendChild(style)
  shadow.appendChild(button)
}
