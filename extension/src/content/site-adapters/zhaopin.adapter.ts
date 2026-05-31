// 智联招聘 (zhaopin.com) DOM adapter
// Stub implementation — selectors to be tuned against live Zhaopin pages

import { BaseSiteAdapter } from './base.adapter'

export class ZhaopinAdapter extends BaseSiteAdapter {
  name = 'zhaopin.com'

  extractAll(): Record<string, string> {
    return {
      name: this.text('.name, .resume-name, h1, [class*="name"]'),
      basicInfo: this.extractSection(['.basic-info', '.info-box', '[class*="basic"]', '[class*="info"]']),
      workExperience: this.extractSection(['.work-list', '.experience-list', '[class*="work"]']),
      education: this.extractSection(['.edu-list', '.education-list', '[class*="edu"]']),
      skills: this.extractSkills(),
      selfDescription: this.text('.self-desc, [class*="self"], [class*="intro"]'),
      salaryExpectation: this.text('[class*="salary"], [class*="expect"]'),
    }
  }

  private extractSection(selectors: string[]): string {
    for (const sel of selectors) {
      const text = this.textAll(sel)
      if (text && text.length > 10) return text
    }
    return ''
  }

  private extractSkills(): string {
    const items = this.list('[class*="skill"], [class*="tag"], [class*="label"]')
    return items.length > 0 ? [...new Set(items)].join(', ') : ''
  }
}
