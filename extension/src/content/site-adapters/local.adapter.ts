// Local test adapter — for demo purposes
// Matches the structure of test_candidate.html

import { BaseSiteAdapter } from './base.adapter'

export class LocalTestAdapter extends BaseSiteAdapter {
  name = 'localhost'

  extractAll(): Record<string, string> {
    return {
      name: this.text('.name') || this.text('h1'),
      basicInfo: this.textAll('.info-detail span'),
      workExperience: this.textAll('.work-experience'),
      education: this.textAll('.education-experience'),
      skills: this.list('.tag-item').join(', '),
      selfDescription: this.text('.self-description'),
      salaryExpectation: this.text('.salary-expect') || this.text('[class*="salary"]'),
    }
  }
}
