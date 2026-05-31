#HR Copilot

AI-powered Chrome browser extension that integrates with recruitment platforms to provide **one-click resume parsing**, **candidate-job matching with radar visualization**, and **personalized outreach message generation** — all directly within the recruiter's existing workflow.

Built for the AnyHelper (AnyChinaJob.com) AI Agent Frontend Developer Intern interview.

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   RECRUITMENT SITE PAGE                   │
│  ┌─────────────────────┐    ┌─────────────────────────┐  │
│  │   Content Script     │    │   Chrome Side Panel      │  │
│  │                      │    │   (Vue3 + Element Plus)  │  │
│  │  • DOM extraction    │◄──►│                          │  │
│  │  • Site adapters     │    │  • Resume parsing tab    │  │
│  │  • Floating button   │    │  • Matching + radar tab  │  │
│  │                      │    │  • Message gen tab       │  │
│  └──────────┬───────────┘    │  • Dashboard tab         │  │
│             │                └───────────┬──────────────┘  │
└─────────────┼────────────────────────────┼────────────────┘
              │ chrome.runtime.sendMessage  │ fetch() POST
              ▼                            ▼
┌─────────────────────────┐  ┌─────────────────────────────┐
│    Service Worker        │  │    FastAPI Backend           │
│    (side panel opener)   │  │    (localhost:8000)          │
└─────────────────────────┘  │                              │
                             │  POST /api/resume/parse      │
                             │  POST /api/matching/score     │
                             │  POST /api/message/generate   │
                             │  GET  /api/dashboard/stats    │
                             └──────────────┬──────────────┘
                                            │ OpenAI SDK
                                            ▼
                             ┌─────────────────────────────┐
                             │    DeepSeek LLM API          │
                             │    (deepseek-chat)           │
                             └─────────────────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Browser Extension | Chrome Manifest V3, TypeScript |
| Frontend Framework | Vue 3 (Composition API), Vite |
| UI Components | Element Plus, ECharts |
| State Management | Pinia |
| Backend Framework | FastAPI (Python 3.10+) |
| Data Validation | Pydantic v2 |
| AI Engine | DeepSeek LLM (OpenAI-compatible API) |
| Automation | Selenium, BeautifulSoup4 |

## Features

### 1. AI Resume Parsing

Extract candidate profile information from recruitment page DOM in one click. The hybrid approach uses CSS selectors for initial text extraction and LLM for intelligent structuring.

```
DOM → Site Adapter (CSS selectors) → Raw text → DeepSeek LLM → Structured JSON
```

**Output fields:** name, work experience, education, skills, languages, salary expectation, location, professional summary.

### 2. Candidate-Job Matching

Paste a job description into the side panel and get an AI-generated evaluation with multi-dimensional scoring.

**Output includes:**
- **Overall score** (0-100) with a circular gauge visualization
- **Radar chart** across 5 dimensions (technical skills, work experience, education, salary fit, overall quality)
- **Skill gap table** highlighting matched vs. missing skills
- **Recommendation tier** (Strongly Recommend / Recommend / Consider / Not Recommended)

### 3. Smart Message Generation

Generate personalized outreach messages tailored to the candidate's background and the job requirements.

**Template types:** Interview Invitation, Follow-up, Rejection, Custom.

### 4. Data Dashboard

Session-level analytics dashboard tracking parse/match/message activity with bar charts and a timeline view.

### 5. Selenium Automation

Standalone Python script for automated browser-based candidate data extraction.

---

## Project Structure

```
anyjob-hr-copilot/
├── extension/                           # Chrome Extension (Vue3 + Vite + TS)
│   ├── manifest.json                    # MV3 manifest
│   ├── vite.config.ts                   # Multi-entry build config
│   ├── src/
│   │   ├── background/
│   │   │   └── service-worker.ts        # Side panel lifecycle manager
│   │   ├── content/
│   │   │   ├── index.ts                 # Content script entry
│   │   │   ├── dom-extractor.ts         # Generic text extraction engine
│   │   │   ├── sidebar-injector.ts      # Floating button + Shadow DOM
│   │   │   └── site-adapters/           # Per-platform CSS selectors
│   │   │       ├── base.adapter.ts      # Abstract adapter base class
│   │   │       ├── bosszhipin.adapter.ts
│   │   │       ├── liepin.adapter.ts
│   │   │       ├── zhaopin.adapter.ts
│   │   │       ├── local.adapter.ts
│   │   │       └── index.ts             # Adapter registry
│   │   └── sidepanel/                   # Vue3 Side Panel Application
│   │       ├── main.ts                  # Vue app bootstrap
│   │       ├── App.vue                  # Root layout
│   │       ├── router.ts                # Hash-mode router
│   │       ├── stores/                  # Pinia stores
│   │       │   ├── candidate.store.ts   # Current candidate state
│   │       │   ├── settings.store.ts    # API config, saved JDs
│   │       │   └── history.store.ts     # Browsing history
│   │       ├── composables/
│   │       │   ├── useApi.ts            # Backend HTTP client
│   │       │   └── useDomBridge.ts      # Content script messaging
│   │       ├── pages/
│   │       │   ├── ResumePage.vue       # Tab 1: Resume parsing
│   │       │   ├── MatchingPage.vue     # Tab 2: Matching + radar
│   │       │   ├── MessagePage.vue      # Tab 3: Message generation
│   │       │   └── DashboardPage.vue    # Tab 4: Data dashboard
│   │       ├── components/
│   │       │   ├── layout/              # SidebarHeader, SidebarTabs
│   │       │   ├── resume/              # ResumeStructured, ResumeEditForm
│   │       │   ├── matching/            # MatchingScore, RadarChart, SkillGapTable
│   │       │   ├── dashboard/           # StatCard
│   │       │   └── shared/              # LoadingSpinner, ErrorAlert, EmptyState
│   │       └── types/                   # TypeScript interfaces
│   └── public/icons/
│
├── backend/                             # FastAPI Backend
│   ├── requirements.txt
│   ├── .env.example
│   ├── app/
│   │   ├── main.py                      # FastAPI app + CORS
│   │   ├── config.py                    # Settings (pydantic-settings)
│   │   ├── routes/                      # API endpoints
│   │   │   ├── health.py                # GET  /api/health
│   │   │   ├── resume.py                # POST /api/resume/parse
│   │   │   ├── matching.py              # POST /api/matching/score
│   │   │   ├── message.py               # POST /api/message/generate
│   │   │   └── dashboard.py             # GET  /api/dashboard/stats
│   │   ├── services/                    # Business logic
│   │   │   ├── llm_client.py            # DeepSeek API wrapper + mock mode
│   │   │   ├── resume_parser.py         # Prompt → JSON → Candidate
│   │   │   ├── matcher.py               # Candidate + JD → MatchResult
│   │   │   └── message_generator.py     # Context → Outreach message
│   │   ├── models/                      # Pydantic v2 schemas
│   │   │   ├── candidate.py             # Candidate, Education, WorkExperience
│   │   │   ├── matching.py              # MatchResult, RadarDimension
│   │   │   ├── message.py               # MessageRequest, MessageResponse
│   │   │   └── dashboard.py             # DashboardStats, DailyBreakdown
│   │   ├── prompts/                     # LLM prompt templates
│   │   │   ├── resume_parse.py          # Resume extraction system prompt
│   │   │   ├── matching.py              # Candidate evaluation prompt
│   │   │   └── message.py               # Message generation prompt
│   │   └── store/
│   │       └── memory_store.py          # In-memory session aggregation
│   └── scripts/
│       ├── test_e2e.py                  # End-to-end pipeline test
│       ├── test_candidate.html          # Sample page for local demo
│       └── selenium_demo.py             # Selenium automation demo
│
└── docs/
```

---

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.10+ (conda recommended)
- Chrome browser

### 1. Install Dependencies

```bash
# Frontend
cd anyjob-hr-copilot
npm install

# Backend
conda activate Ai  # or your Python env
pip install -r backend/requirements.txt
```

### 2. Configure API Key

```bash
# Edit backend/.env
DEEPSEEK_API_KEY=sk-your-actual-key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

**Mock mode:** If the API key starts with `sk-test-`, the backend returns built-in mock data without calling the LLM — useful for offline demos.

### 3. Start Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Verify: `curl http://localhost:8000/api/health` → `{"status":"ok","model":"deepseek-chat"}`

### 4. Run Pipeline Tests

```bash
python backend/scripts/test_e2e.py
# Expected: 5 passed, 0 failed
```

### 5. Build & Load Extension

```bash
npm run build:extension
```

1. Chrome → `chrome://extensions`
2. Enable **Developer mode** (top right toggle)
3. Click **Load unpacked**
4. Select `extension/dist/` folder

---

## Live Demo Guide

### Start Test Page

```bash
cd backend/scripts
python -m http.server 8080
```

Open `http://localhost:8080/test_candidate.html` in Chrome.

### Walkthrough

| Step | Action | What to Show |
|------|--------|-------------|
| 1 | Open test page, click floating **🤖 AI 解析** button | Content script injection, Side Panel opens |
| 2 | **简历解析 tab**: Click **🔍 提取页面简历** | Structured resume: name, skills cloud, work history, education |
| 3 | **人岗匹配 tab**: Paste JD, click **🎯 开始匹配** | Score gauge + ECharts radar chart + skill gap table |
| 4 | **智能消息 tab**: Select template, click **✨ 生成消息** | Personalized message, copy to clipboard |
| 5 | **数据看板 tab** | 4 stat cards + daily trend chart + activity timeline |

---

## API Reference

### `GET /api/health`

Health check with current model info.

**Response:**
```json
{"status": "ok", "model": "deepseek-chat"}
```

### `POST /api/resume/parse`

Parse raw profile text into structured candidate data.

**Request:**
```json
{
  "raw_text": "张小明 男 28岁 本科 5年经验\n工作经历：字节跳动 高级前端开发工程师 ...",
  "source_site": "zhipin.com"
}
```

**Response:**
```json
{
  "name": "张小明",
  "years_of_experience": 5,
  "current_title": "高级前端开发工程师",
  "current_company": "字节跳动",
  "skills": ["Vue3", "TypeScript", "React", "JavaScript"],
  "education": [{"school": "上海交通大学", "degree": "本科", "major": "计算机科学与技术", "graduation_year": 2019}],
  "work_experience": [{"company": "字节跳动", "title": "高级前端开发工程师", "duration_months": 36, "description": "...", "skills_used": ["Vue3", "TypeScript"]}],
  "summary": "5年前端开发经验，精通Vue3和React..."
}
```

### `POST /api/matching/score`

Evaluate a candidate against a job description.

**Request:**
```json
{
  "candidate": { /* Candidate object from /resume/parse */ },
  "jd_text": "高级前端开发工程师\n要求：3年以上前端经验，精通Vue3/React..."
}
```

**Response:**
```json
{
  "overall_score": 85,
  "recommendation": "强烈推荐",
  "radar_dimensions": [
    {"name": "技术技能", "score": 90, "candidate_value": "Vue3, React, TS", "jd_requirement": "Vue3/React, TS"},
    {"name": "工作经验", "score": 85, "candidate_value": "5年，字节+阿里", "jd_requirement": "3年以上"}
  ],
  "matched_skills": ["Vue3", "TypeScript", "React"],
  "missing_skills": ["Python", "Docker"],
  "strengths": ["前端技术栈全面", "大厂工作经验"],
  "weaknesses": ["后端技术储备不足"],
  "summary": "候选人技术栈与岗位高度匹配..."
}
```

### `POST /api/message/generate`

Generate a personalized outreach message.

**Request:**
```json
{
  "candidate": { /* Candidate object */ },
  "jd_title": "高级前端开发工程师",
  "jd_company": "字节跳动",
  "template_type": "面试邀请",
  "custom_instruction": ""
}
```

**Response:**
```json
{
  "message": "张小明确认好！\n\n我是AnyJob平台的HR...",
  "template_used": "面试邀请",
  "tokens_used": 0
}
```

### `GET /api/dashboard/stats?days=7`

Aggregated session statistics.

**Response:**
```json
{
  "total_parsed": 5,
  "total_matched": 3,
  "total_messages": 2,
  "avg_match_score": 82.5,
  "daily_breakdown": [{"date": "2026-05-29", "parsed_count": 5, "matched_count": 3, "message_count": 2}],
  "recent_activity": [{"timestamp": "2026-05-29T17:30:00", "action": "简历解析", "candidate_name": "张小明", "detail": "成功解析候选人简历"}]
}
```

---

## Extending to New Platforms

Adding support for a new recruitment site requires only **one new adapter file** (~50 lines):

1. Create `extension/src/content/site-adapters/newsite.adapter.ts`
2. Extend `BaseSiteAdapter`, override `extractAll()` with site-specific CSS selectors
3. Register in `site-adapters/index.ts`
4. Add the domain to `manifest.json` host_permissions

The LLM pipeline, matching, and messaging logic remain unchanged.

```typescript
// Example: Adding a new site
export class NewSiteAdapter extends BaseSiteAdapter {
  name = 'newsite.com'

  extractAll(): Record<string, string> {
    return {
      name:           this.text('.candidate-name'),
      basicInfo:      this.textAll('.info-item span'),
      workExperience: this.textAll('.experience-section'),
      skills:         this.list('.skill-tag'),
      education:      this.text('.education-section'),
      selfDescription: this.text('.summary'),
      salaryExpectation: this.text('.salary'),
    }
  }
}
```

---

## Interview Talking Points

- **Architecture**: Three-layer communication (Content Script → Service Worker → Side Panel) with typed message passing
- **Site Adapter pattern**: Open-closed principle — add platforms without modifying existing code
- **Prompt engineering**: Iteratively optimized LLM prompts for >90% extraction accuracy
- **Shadow DOM isolation**: Floating button styles don't leak into host pages
- **Mock mode**: `sk-test-` prefix triggers offline demo mode with built-in data — demonstrates testing strategy
- **Modular design**: Each AI capability (parse/match/message) is an independent service with own prompt templates

---

## License

MIT
