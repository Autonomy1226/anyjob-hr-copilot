# AnyJob HR Copilot — Interview Preparation Guide (English)

---

## Part 1: Project Presentation (Verbal Script)

### 1.1 60-Second Elevator Pitch

> I independently built **AnyJob HR Copilot** — an AI-powered Chrome browser extension for HR recruitment. It integrates directly into major Chinese recruitment platforms like BOSS Zhipin and Liepin, giving recruiters three core AI capabilities: one-click resume parsing, candidate-job matching with radar visualization, and personalized outreach message generation.
>
> The tech stack is fully aligned with your job requirements: Chrome Manifest V3 + Vue 3 with Element Plus for the frontend, FastAPI + Python for the backend, DeepSeek's LLM as the AI engine, and Selenium for automation. I handled the entire development lifecycle from architecture design to implementation — 66 source files, end-to-end pipeline tests all passing.

### 1.2 Three-Minute Detailed Walkthrough

#### Opening (30 sec)

> The problem I'm solving is simple but widespread: recruiters waste hours switching between tabs, manually copying candidate data, and composing individual messages on recruitment platforms. My extension puts an AI assistant right in the sidebar of those platforms — the recruiter never needs to leave their workflow.

#### Core Features (90 sec)

**Feature 1: AI Resume Parsing**
> When a recruiter browses a candidate profile, the content script detects the page, injects a floating "AI Parse" button, and extracts the candidate's data from the page DOM using platform-specific CSS selectors. The raw text is sent to a FastAPI backend, where DeepSeek's LLM parses it into structured JSON — name, work history with company/title/duration, education, skills, salary expectations, and a professional summary. The entire round-trip takes about 2-3 seconds.

> I chose a hybrid approach: DOM extraction guarantees data provenance, while the LLM handles inconsistent formatting and semantic understanding that pure regex or rule-based extraction can't.

**Feature 2: Candidate-Job Matching**
> The recruiter pastes a job description into the side panel. The system evaluates the candidate across five dimensions: technical skills, work experience, education background, salary alignment, and overall quality. The output includes a 0-100 match score displayed as a circular gauge, an interactive ECharts radar chart showing dimension-level performance, and a skill gap table that clearly marks which requirements are met and which are missing. Each dimension includes the specific evidence — what the candidate offers versus what the JD requires — so the evaluation is transparent and auditable.

**Feature 3: Smart Message Generation**
> Based on the candidate's profile and the job context, the system generates a personalized outreach message with a single click. There are four template types: interview invitation, follow-up, rejection, and custom. The recruiter can review and edit the generated message, then copy it to the recruitment platform's chat with one click. This reduces message drafting time from an average of 5 minutes to about 10 seconds.

**Feature 4: Dashboard + Selenium Automation**
> A session-level analytics dashboard tracks key metrics: total resumes parsed, matches evaluated, messages generated, and average match score — all visualized with ECharts bar charts and a timeline. I also built a standalone Selenium script that automates the full pipeline: launch browser, navigate to a candidate page, extract data, call the API, and produce structured output — demonstrating automation capability without requiring the extension to be installed.

#### Architecture Highlights (60 sec)

> The architecture uses a three-layer communication model: the Content Script handles DOM extraction and button injection with Shadow DOM isolation, the Service Worker manages the side panel lifecycle, and the Side Panel is a Vue 3 single-page application with four tabs and twelve components, using Pinia for state management.

> The key design pattern is the **Site Adapter pattern**. Each recruitment platform needs only a ~50-line adapter class defining its CSS selectors. The entire downstream pipeline — LLM parsing, matching, messaging — is completely reused. This follows the open-closed principle: adding a new platform requires zero changes to existing code.

> On the backend, each AI capability (parsing, matching, messaging) is an independent service with its own prompt templates, making them easy to debug and optimize individually. I also built a mock mode: when the API key starts with `sk-test-`, the backend returns built-in mock data without calling the LLM — useful for offline demos and testing.

---

## Part 2: Common Interview Questions & Answers

### Q1: Walk me through this project. What did you build?

**A:** I built HR Copilot, an AI-powered Chrome extension for HR recruiters. I was responsible for:

- **Architecture**: Designed the MV3 three-layer communication model from scratch (Content Script → Service Worker → Side Panel)
- **Frontend**: Built the side panel UI with Vue 3 + Element Plus — 4 feature tabs, 12 components
- **Backend**: Built 5 API endpoints with FastAPI, designed 3 sets of LLM prompt templates
- **AI Integration**: Integrated DeepSeek LLM via the OpenAI SDK for resume parsing, match evaluation, and message generation
- **Automation**: Developed a Selenium + BeautifulSoup data extraction script
- **Testing**: Wrote end-to-end pipeline tests covering all 5 endpoints

My key technical decision was choosing a hybrid "DOM extraction + LLM structuring" approach rather than pure LLM — DOM guarantees data provenance, while the LLM handles semantic understanding.

---

### Q2: What was the most challenging part? How did you solve it?

**A:** Three major challenges:

**Challenge 1: Chrome Side Panel API communication.** The Side Panel API in MV3 is relatively new with sparse documentation. Content Script and Side Panel message passing requires routing through the Service Worker. I built a type-safe message bridge layer (`useDomBridge` composable) that wraps `chrome.runtime.sendMessage` and `chrome.tabs.sendMessage` with unified error handling and timeout logic.

**Challenge 2: LLM output reliability.** DeepSeek occasionally returns malformed JSON. I implemented JSON validation with automatic retry in `llm_client.py` — up to 2 retries, with the retry message explicitly asking the LLM to fix the JSON format. I also built mock mode for offline development.

**Challenge 3: Style isolation.** The extension's floating button is injected into third-party pages and must not leak styles. I used Shadow DOM to create an isolated style scope — all CSS lives inside the shadow root and cannot conflict with the host page.

---

### Q3: Why Chrome Manifest V3? What are its advantages over V2?

**A:** V3 is mandatory going forward — Chrome Web Store stopped accepting new V2 extensions in 2024 and is phasing out existing ones through 2025. Technical advantages:
- **Service Worker over Background Page**: Event-driven, doesn't persist in memory, more resource-efficient
- **Side Panel API**: Native side panel support, more stable than manually injecting iframes (the V2 approach)
- **Finer-grained permissions**: `host_permissions` declared separately, users can grant selectively
- **Improved security model**: No remotely-hosted code, no eval()

---

### Q4: What security measures did you implement?

**A:**
- **Shadow DOM isolation**: Floating button CSS is fully encapsulated, no style leakage
- **Principle of least privilege**: Only 5 permissions declared, host_permissions limited to target recruitment platforms
- **API key management**: Key stored in `.env`, excluded from Git via `.gitignore`
- **CORS middleware**: Backend only allows extension-origin requests
- **Sandboxed Side Panel**: Chrome's native side panel sandbox isolates from the host page

---

### Q5: What would it take to productionize this project?

**A:** MVP → production requires:
1. **Database**: Replace in-memory store with PostgreSQL/MySQL for persistence
2. **Auth system**: User registration/login, API key management, multi-tenant isolation
3. **Platform tuning**: Test and refine CSS selectors on live BOSS Zhipin and Liepin pages
4. **Chrome Web Store**: Prepare listing assets, pass Chrome review
5. **Caching**: Cache parsed resumes by candidate ID hash to avoid redundant LLM calls
6. **Error monitoring**: Sentry or similar for frontend and backend exceptions
7. **Compliance**: Ensure PIPL (Personal Information Protection Law) compliance — resume data is sensitive

---

### Q6: How did you approach prompt engineering?

**A:** I designed independent System + User prompt pairs for each AI capability:

**Resume Parsing Prompt:**
- System prompt defines an exact JSON schema with 17 typed fields
- Includes specific rules: "Normalize company names", "Categorize skills meaningfully", "Infer years_of_experience from work history"
- Ends with: "Return ONLY the JSON object, no additional text"

**Matching Prompt:**
- Five evaluation dimensions with specific scoring guidelines
- Requires both `candidate_value` and `jd_requirement` for each dimension (forces evidence-based scoring)
- Fixed recommendation tiers for consistent UI display

**Quality Assurance:**
- All LLM responses validated through Pydantic v2 `model_validate()`
- Automatic retry (max 2) on JSON parse failure
- `response_format={"type": "json_object"}` parameter constrains output format

---

### Q7: How did you use Vue 3's Composition API in this project?

**A:** The entire project uses Composition API with `<script setup>`:

- **Composables**: `useApi()` encapsulates all backend HTTP calls, `useDomBridge()` encapsulates content script messaging. Each composable has a single responsibility and is independently testable.
- **Pinia Stores**: All three stores (`candidateStore`, `settingsStore`, `historyStore`) use the setup function syntax, sharing reactive state across components.
- **Reactive data flow**: API results → update Pinia Store → components auto-render. For resume parsing: `extractionStatus: 'loading'` → shows LoadingSpinner → `extractionStatus: 'done'` → shows ResumeStructured.

---

### Q8: How does Content Script ↔ Side Panel communication work?

**A:** In Chrome MV3, Content Scripts and the Side Panel run in separate contexts:

**Opening the side panel:**
```
User clicks floating button
  → Content Script: chrome.runtime.sendMessage({ type: 'OPEN_SIDE_PANEL' })
  → Service Worker: chrome.runtime.onMessage → chrome.sidePanel.open({ tabId })
  → Side Panel renders
```

**Requesting DOM data:**
```
User clicks "Parse Resume"
  → Side Panel (useDomBridge): chrome.tabs.sendMessage(tabId, { type: 'EXTRACT_DOM' })
  → Content Script: chrome.runtime.onMessage → Site Adapter → sendResponse(data)
  → Side Panel: receives rawText → calls useApi().parseResume()
```

These calls are wrapped in `useDomBridge.ts` as typed Promise interfaces — upper-layer code never touches `chrome.runtime` directly.

---

### Q9: How would you optimize performance?

**A:**
- **UI**: Element Plus components tree-shaken by Vite, ECharts modules imported individually (not the full bundle)
- **Network**: `useApi` composable manages request deduplication; candidate ID hash caching for LLM results (future)
- **DOM**: Site Adapters use precise `querySelector` calls, no full-page traversal
- **Build**: The 1.5MB `sidepanel.js` chunk is the main bottleneck — can be split via `manualChunks` or dynamic imports in production

---

### Q10: What engineering skills does this project demonstrate?

**A:**
1. **Frontend engineering**: Scaffolding to build configuration, full development lifecycle
2. **Architecture design**: Three-layer communication model + Adapter pattern + service-oriented backend
3. **AI engineering**: Prompt engineering + schema validation + retry logic + mock mode
4. **Full-stack capability**: Independent frontend and backend development
5. **Testing mindset**: E2E pipeline tests with 100% endpoint coverage
6. **Documentation**: Bilingual README + architecture diagrams + API specs

---

## Part 3: Job-Specific Questions & Answers

### JD Responsibility 1: Browser Extension Development

**Q: What is your browser extension development workflow?**

**A:** The standard workflow: requirements → manifest.json design (permissions, host_permissions, content_script matching rules) → content script development (DOM manipulation, messaging) → service worker (event handling, lifecycle) → UI development (Popup/Side Panel/Options) → local testing (chrome://extensions) → packaging and publishing.

I follow this rigorously. My manifest V3 declares minimal permissions; content scripts inject at `document_idle` to ensure DOM readiness.

**Q: What are the differences between Firefox and Chrome extension development?**

**A:** Both follow the WebExtensions standard but differ in:
- Firefox uses `browser.*` API namespace vs Chrome's `chrome.*`
- Firefox uses `sidebar_action` instead of Chrome's Side Panel API
- Firefox has limited Service Worker support, sometimes requiring Background Pages
- In my project, the communication layer is abstracted (`useDomBridge` composable), so swapping the underlying API doesn't affect upper-layer logic.

---

### JD Responsibility 2: Frontend Design + Data Visualization

**Q: Why Vue 3 over React for this project?**

**A:** Vue 3's Composition API with `<script setup>` offers more concise component logic. Element Plus provides a complete UI component library with excellent Chinese ecosystem support. Pinia's intuitive state management aligns well with Composition API patterns.

However, I'm comfortable with React as well. If the team uses React, I can rebuild the UI layer with React + Ant Design while reusing the entire architecture (Site Adapter pattern, messaging, API layer).

**Q: How did you implement the ECharts radar chart?**

**A:** Using `vue-echarts` with on-demand module imports (RadarChart, Title, Tooltip, etc.) to minimize bundle size. The component receives `radar_dimensions` as a prop, transforms it into ECharts' `radar.indicator` and `series` configuration. Two data lines: blue solid line (candidate scores) + gray dashed line (JD baseline at 70), making the comparison immediately visible.

---

### JD Responsibility 3: API Integration & Async Programming

**Q: What issues did you encounter during frontend-backend integration?**

**A:** Primarily type synchronization. TypeScript interfaces and Pydantic models are defined separately. My approach: define Pydantic models as the single source of truth on the backend, then mirror them as TypeScript interfaces on the frontend. Use `model_validate()` at runtime to ensure backend output matches the schema.

**Q: How do you handle async request errors?**

**A:** Centralized in `useApi.ts`:
- HTTP errors: check `res.ok`, parse `detail` field for meaningful messages
- Network errors: caught by `fetch()`, re-thrown to callers
- LLM errors: retry logic on backend (max 2), final failure returns 500
- UI layer: each page manages independent `status: 'idle' | 'loading' | 'done' | 'error'` state, showing ErrorAlert on failure

---

### JD Responsibility 4: Selenium Automation

**Q: How is Selenium used in this project?**

**A:** I built a standalone demo script (`selenium_demo.py`) that:
1. Launches Chrome via Selenium WebDriver
2. Navigates to a recruitment candidate page (or loads a local HTML file)
3. Extracts profile text using BeautifulSoup
4. Calls the backend API for resume parsing → matching → message generation
5. Prints structured results

This demonstrates the full automated data collection pipeline.

**Q: How do you handle anti-scraping measures?**

**A:** BOSS Zhipin and similar sites employ anti-debugging and anti-scraping. My approach:
1. **Design principle**: The extension assists users who are already logged in and authorized — it's an augmentation tool, not a scraper
2. **Selenium anti-detection**: Pass `--disable-blink-features=AutomationControlled`, remove `navigator.webdriver` flag
3. **Human-like pacing**: Randomized intervals between actions
4. **Graceful degradation**: If CSS selectors fail (site redesign), the adapter returns empty strings, and the LLM provides semantic fallback

---

### JD Responsibility 5: Cross-Border Team Collaboration

**Q: Do you have experience writing English technical documentation?**

**A:** Yes — this project's documentation is fully bilingual:
- `README.md` (English) and `README_CN.md` (Chinese), each ~300 lines
- Code comments in English where present
- Git commits follow conventional commit format in English
- API documentation includes complete English request/response examples
- Architecture documentation is written for an international audience

**Q: How would you collaborate across time zones?**

**A:** I would:
- Prefer async communication (Slack, Notion, GitHub Issues) to reduce sync meeting dependency
- Write design docs and API specs before coding to minimize alignment needs
- Leave sufficient context in code reviews to reduce back-and-forth
- Use video calls for key milestones, text for day-to-day

---

### Bonus 1: LLM Application Development

**Q: What is your understanding of LLM application development?**

**A:** I believe LLM app development isn't about calling an API — it's about solving three engineering problems:
1. **Prompt Engineering**: Design system prompts that constrain behavior and output format; inject precise context via user prompts
2. **Reliability**: LLMs are non-deterministic — you need JSON schema constraints + format validation + automatic retry + graceful degradation
3. **Product Integration**: LLMs are tools, not products. The real value is embedding LLM capabilities into the user's existing workflow. This project is a textbook case: the recruiter doesn't open ChatGPT and type prompts — they click one button while browsing and get results instantly.

**Q: Why DeepSeek instead of GPT-4?**

**A:** Three reasons:
1. **Cost**: DeepSeek's API pricing is significantly lower, critical for high-frequency use (recruiters may parse dozens of resumes daily)
2. **Chinese capability**: DeepSeek excels at Chinese language tasks — essential for Chinese HR/recruitment content
3. **API compatibility**: OpenAI-compatible endpoint means the code uses the OpenAI SDK — switching to another model is a one-line `base_url` change

---

### Bonus 2: Low-Code Platform Understanding

**Q: What do you know about low-code platforms? How does this project relate?**

**A:** Low-code platforms reduce development barriers through visual drag-and-drop and configuration-based building.

In this project, the **message template system** is a lightweight low-code concept: recruiters configure message templates (type selection, custom instructions) in the UI without writing any code. Further extensions could include:
- Visual template editor (drag text blocks, variable placeholders)
- Template marketplace (share and reuse templates)
- Conditional logic (auto-select template based on match score range)

If the team has low-code platform products, I can apply this experience directly.

---

## Part 4: Quick Self-Checklist

Before the interview, verify you can:

- [ ] Explain what the project is and what problem it solves — in 60 seconds
- [ ] Draw the architecture diagram and explain the three-layer communication model
- [ ] Explain the Site Adapter pattern and how to extend to new platforms
- [ ] Describe your prompt engineering approach
- [ ] Explain Shadow DOM isolation and why it matters
- [ ] Justify every technology choice: Vue 3, DeepSeek, MV3, Selenium
- [ ] Articulate what's needed to go from MVP to production
- [ ] Present the project fluently in both Chinese and English
- [ ] Share 1-2 specific problems you encountered and how you solved them
- [ ] Run the project locally and complete the E2E demo

---

## Part 5: AI Agent Engineer Questions & Answers

> These questions probe whether you genuinely understand AI-assisted development — not just whether you've used AI tools, but how and why.

### QA1: "How do you use AI tools in your development workflow?"

**A:** I practice what I call **AI-Native Engineering** — a systematic collaboration workflow, not "ask ChatGPT when stuck."

**Layer 1: AI for architecture exploration.** When designing the Chrome extension sidebar, I described the requirements to an AI Plan agent. It surfaced three approaches (Side Panel API / iframe injection / popup) with trade-off analysis. I chose Side Panel API. AI provided information; I made the decision.

**Layer 2: AI for scaled code generation.** ~60% of this project's code scaffold was AI-generated: CRUD routes, Vue component templates, TypeScript interfaces, Pydantic models. These are highly templated patterns — AI generates them reliably; human review suffices. The remaining ~40% I wrote manually: core communication logic, LLM prompts, error handling — these require architecture-level judgment.

**Layer 3: AI for accelerated debugging.** I feed error stacks + context to AI for instant root-cause analysis. Example: `httpx.AsyncClient.__init__() got unexpected keyword argument 'proxies'` → AI immediately identified openai/httpx version incompatibility → one-line fix. Manual debugging would have been 20+ minutes.

**Layer 4: AI for documentation.** README, API docs, interview prep — all AI-generated first drafts. I reviewed and supplemented with engineering insights and quantified data.

**Core philosophy**: AI is a lever, not a replacement. Same 2-week timeline — a traditional developer might finish the frontend pages; an AI-Native developer delivers a 66-file complete MVP. That's the difference.

### QA2: "How do you ensure the quality of AI-generated code?"

**A:** Three gates:

1. **Type system as first defense**: TypeScript compilation + Pydantic v2 runtime validation. If AI-generated code has type mismatches, it fails at compile/startup.
2. **E2E tests covering the data flow**: 5-step pipeline test validates the complete DOM → LLM → JSON → UI chain. Run after every change.
3. **Core code never delegated**: Message bridge (`useDomBridge`), prompt templates, error handling — I write these manually. AI handles "filling"; I handle "scaffolding."

### QA3: "If AI wrote 60% of the code, what was your contribution?"

**A:** Code volume doesn't equal engineering value. My contribution is in five areas:

1. **Architecture decisions**: Three-layer communication model, Site Adapter pattern, hybrid extraction pipeline. AI lists options; I choose.
2. **Prompt design**: The three System Prompts are the product's core "code." AI can't write quality prompts — it requires domain understanding (HR workflows) and iterative experimentation.
3. **Test design**: What to test, how to mock, how to validate — these are engineering judgments.
4. **Quality control**: AI-generated code passes TypeScript compilation + Pydantic validation + human review — three gates.
5. **Integration**: Wiring AI-generated modules into a complete product pipeline.

**Simple framing: AI executes. I design, decide, and validate.**

### QA4: "How did you test this project? Where do your numbers come from?"

**A:** Every metric has a specific measurement method and validation process:

**Pipeline test pass rate (100%)**: Run `test_e2e.py` — 5 steps covering all API endpoints with mock mode (no API key needed).

**Resume extraction accuracy (90%+)**: Prepared 5 diverse candidate texts (big-tech, fresh grad, career changer, non-standard format, mixed Chinese/English). Manually checked all 17 fields per response. Pydantic validation as automated guardrail. Conservative estimate based on test results.

**Token reduction (70%)**: Calculated. Raw HTML ~3,200 chars (~2,400 tokens). After DOM pre-extraction ~390 chars (~500 tokens). With system prompts: (3,000 - 800) / 3,000 ≈ 73%. The architecture decision had a cost model behind it.

**Message drafting (5 min → 10 sec)**: Workflow analysis. Traditional: review resume (30s) + match JD (30s) + write (2-3 min) + proofread (1 min) = 4-5 min. Extension: click (1s) + LLM (2s) + confirm (5-10s) = ~10s. 30x gap comes from eliminating the manual writing step.

**Shadow DOM isolation (100%)**: Added `button { background: red !important }` to test page. Button maintained original style → zero leakage.

**Key principle: I don't claim numbers I haven't verified. Where precise measurement is possible, I give the number. Where it's an estimate, I give a conservative figure and explain the derivation.**

### QA5: "What's your take on Vibe Coding?"

**A:** "Vibe Coding" is about describing intent in natural language, letting AI generate code, and iterating rapidly toward the target. I agree with the direction, but I don't see it as "not writing code" — it's **shifting coding from manual typing to conversation-driven iteration.**

In this project:
- Used Vibe Coding for scaffolding ("Create a Vue3 + TS Chrome extension project with Vite" → AI generates → verify → done)
- Did NOT rely on AI for core communication logic (Chrome MV3's three-context messaging — AI often gets this wrong)
- Used AI for bug diagnosis, but judged fixes myself

**Vibe Coding is a speed tool, not a quality substitute.** Go fast where you can; own the critical parts yourself.

### QA6: "If you could add one AI Agent capability to this project, what would it be?"

**A:** A **multi-turn conversational Interview Agent**. Currently, message generation is "one-click → one message." I'd upgrade it to:

> HR selects candidate → Agent auto-sends initial outreach → candidate replies → Agent analyzes reply intent (interested / hesitant / declined) → auto-generates follow-up response → loops until interview is confirmed → Agent auto-sends calendar invite.

Technical implementation:
- Conversation state machine for multi-turn interaction management
- LLM for intent recognition and reply generation
- Tool calling: Agent queries calendar availability, sends emails
- Human-in-the-loop: all messages confirmed by HR before sending (safety boundary)

This directly relates to AnyHelper's business — cross-border recruitment involves high-volume initial candidate communication. An Agent could handle ~80% of the repetitive work.

---

## Appendix: Glossary

| Chinese | English |
|---------|---------|
| 浏览器插件 | Browser Extension |
| 内容脚本 | Content Script |
| 服务工作者 | Service Worker |
| 侧边栏面板 | Side Panel |
| 清单文件 V3 | Manifest V3 |
| 影子 DOM | Shadow DOM |
| 提示词工程 | Prompt Engineering |
| 简历解析 | Resume Parsing |
| 人岗匹配 | Candidate-Job Matching |
| 话术生成 | Message Generation |
| 雷达图 | Radar Chart |
| 数据看板 | Dashboard |
| 适配器模式 | Adapter Pattern |
| 开闭原则 | Open-Closed Principle |
| 组合式 API | Composition API |
| 状态管理 | State Management |
