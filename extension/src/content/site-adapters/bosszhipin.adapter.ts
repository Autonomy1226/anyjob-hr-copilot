// BOSS直聘 (zhipin.com) DOM adapter
// Selectors based on common BOSS直聘 candidate profile page structure

import { BaseSiteAdapter } from './base.adapter'

export class BosszhipinAdapter extends BaseSiteAdapter {
  name = 'zhipin.com'

  extractAll(): Record<string, string> {
    return {
      name: this.extractName(),
      basicInfo: this.extractBasicInfo(),
      workExperience: this.extractWorkExperience(),
      education: this.extractEducation(),
      skills: this.extractSkills(),
      selfDescription: this.extractSelfDescription(),
      salaryExpectation: this.extractSalary(),
    }
  }

  private extractName(): string {
    return (
      this.text('.name') ||
      this.text('.candidate-name') ||
      this.text('[class*="name"] h1') ||
      this.text('h1')
    )
  }

  private extractBasicInfo(): string {
    const parts: string[] = []

    // Age, gender, location, years of experience
    const infoItems = document.querySelectorAll(
      '.info-detail li, .basic-info .item, .resume-info .info-item, [class*="info"] span'
    )
    infoItems.forEach((el) => {
      const t = el.textContent?.trim()
      if (t) parts.push(t)
    })

    // Fallback: try common containers
    if (parts.length === 0) {
      const containers = document.querySelectorAll(
        '.resume-info, .basic-info, .info-box, [class*="basic"]'
      )
      containers.forEach((c) => {
        const t = c.textContent?.trim()
        if (t) parts.push(t)
      })
    }

    return parts.join(' | ')
  }

  private extractWorkExperience(): string {
    // Try common work experience container selectors
    const selectors = [
      '.work-list .work-item',
      '.experience-list .exp-item',
      '[class*="work"] [class*="item"]',
      '.work-experience',
      '[class*="experience"]',
    ]

    for (const sel of selectors) {
      const el = document.querySelector(sel)
      if (el) {
        const text = el.textContent?.trim()
        if (text && text.length > 10) return text
      }
    }

    // Broad fallback
    const broadMatches = document.querySelectorAll(
      '[class*="work"], [class*="job"], [class*="experience"], [class*="经历"]'
    )
    const texts: string[] = []
    broadMatches.forEach((el) => {
      const t = el.textContent?.trim()
      if (t && t.length > 20) texts.push(t)
    })
    return texts.join('\n---\n')
  }

  private extractEducation(): string {
    const selectors = [
      '.edu-list .edu-item',
      '.education-list .edu-item',
      '[class*="edu"] [class*="item"]',
      '.education-experience',
      '[class*="education"]',
    ]

    for (const sel of selectors) {
      const text = this.textAll(sel)
      if (text && text.length > 5) return text
    }

    const broadMatches = document.querySelectorAll('[class*="edu"], [class*="school"], [class*="教育"]')
    const texts: string[] = []
    broadMatches.forEach((el) => {
      const t = el.textContent?.trim()
      if (t && t.length > 5) texts.push(t)
    })
    return texts.join('\n')
  }

  private extractSkills(): string {
    const selectors = [
      '.tag-list .tag-item',
      '.skill-tags .skill-item',
      '[class*="skill"] [class*="tag"]',
      '[class*="tag"]',
    ]

    for (const sel of selectors) {
      const items = this.list(sel)
      if (items.length > 0) return items.join(', ')
    }

    const broadMatches = document.querySelectorAll('[class*="skill"], [class*="tag"], [class*="label"], [class*="tech"]')
    const texts: string[] = []
    broadMatches.forEach((el) => {
      const t = el.textContent?.trim()
      if (t && t.length > 1 && t.length < 30) texts.push(t)
    })
    return [...new Set(texts)].join(', ')
  }

  private extractSelfDescription(): string {
    return (
      this.text('.self-description') ||
      this.text('.self-desc') ||
      this.text('[class*="self"]') ||
      this.text('[class*="description"]') ||
      this.text('[class*="intro"]') ||
      this.text('[class*="summary"]') ||
      ''
    )
  }

  private extractSalary(): string {
    return (
      this.text('[class*="salary"]') ||
      this.text('[class*="expect"]') ||
      this.text('[class*="hope"]') ||
      ''
    )
  }
}
