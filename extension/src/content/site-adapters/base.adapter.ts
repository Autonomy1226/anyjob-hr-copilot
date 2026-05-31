// Abstract base class for site-specific DOM adapters
// Each recruitment platform gets its own adapter with CSS selectors

export interface SiteAdapter {
  name: string
  extractAll(): Record<string, string>
}

export abstract class BaseSiteAdapter implements SiteAdapter {
  abstract name: string

  abstract extractAll(): Record<string, string>

  protected text(selector: string): string {
    const el = document.querySelector(selector)
    return el?.textContent?.trim() || ''
  }

  protected textAll(selector: string): string {
    const els = document.querySelectorAll(selector)
    return Array.from(els)
      .map((el) => el.textContent?.trim())
      .filter(Boolean)
      .join('\n')
  }

  protected list(selector: string): string[] {
    const els = document.querySelectorAll(selector)
    return Array.from(els)
      .map((el) => el.textContent?.trim())
      .filter((t): t is string => !!t)
  }
}
