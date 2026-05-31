// Generic DOM-to-text extraction engine
// Uses site-specific adapters for CSS selectors, then cleans and normalizes the output

import type { SiteAdapter } from './site-adapters/base.adapter'

export class DomExtractor {
  constructor(private adapter: SiteAdapter) {}

  extract(): string {
    const sections = this.adapter.extractAll()
    return this.buildRawText(sections)
  }

  private buildRawText(sections: Record<string, string>): string {
    const parts: string[] = []

    for (const [key, value] of Object.entries(sections)) {
      if (value?.trim()) {
        parts.push(`--- ${key} ---\n${value.trim()}`)
      }
    }

    return parts.join('\n\n')
  }
}
