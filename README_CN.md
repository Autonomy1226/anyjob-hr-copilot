<div align="right">
  <a href="./README.md">🇬🇧 English</a>
</div>

# HR Copilot

一款面向 HR 招聘场景的 AI Copilot 浏览器插件，集成在主流招聘平台中，提供 **一键简历解析**、**人岗匹配评估（含雷达图）**、**个性化沟通话术生成** 等 AI 辅助功能，大幅提升招聘效率。

本项目为 AnyHelper（AnyChinaJob.com）AI Agent 前端开发实习生面试作品。

---

## 系统架构

```
┌──────────────────────────────────────────────────────────┐
│                    招聘网站页面                           │
│  ┌─────────────────────┐    ┌─────────────────────────┐  │
│  │   Content Script     │    │   Chrome 侧边栏          │  │
│  │                      │    │   (Vue3 + Element Plus)  │  │
│  │  • DOM 信息提取      │◄──►│                          │  │
│  │  • 站点适配器        │    │  • 简历解析标签页        │  │
│  │  • 浮动触发按钮      │    │  • 人岗匹配 + 雷达图     │  │
│  │                      │    │  • 智能消息标签页        │  │
│  └──────────┬───────────┘    │  • 数据看板标签页        │  │
│             │                └───────────┬──────────────┘  │
└─────────────┼────────────────────────────┼────────────────┘
              │ chrome.runtime.sendMessage  │ fetch() POST
              ▼                            ▼
┌─────────────────────────┐  ┌─────────────────────────────┐
│    Service Worker        │  │    FastAPI 后端              │
│    (侧边栏生命周期管理)   │  │    (localhost:8000)          │
└─────────────────────────┘  │                              │
                             │  POST /api/resume/parse      │
                             │  POST /api/matching/score     │
                             │  POST /api/message/generate   │
                             │  GET  /api/dashboard/stats    │
                             └──────────────┬──────────────┘
                                            │ OpenAI SDK
                                            ▼
                             ┌─────────────────────────────┐
                             │    DeepSeek 大模型 API       │
                             │    (deepseek-chat)           │
                             └─────────────────────────────┘
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 浏览器插件 | Chrome Manifest V3, TypeScript |
| 前端框架 | Vue 3 (Composition API), Vite |
| UI 组件库 | Element Plus, ECharts |
| 状态管理 | Pinia |
| 后端框架 | FastAPI (Python 3.10+) |
| 数据校验 | Pydantic v2 |
| AI 引擎 | DeepSeek LLM (兼容 OpenAI SDK) |
| 自动化工具 | Selenium, BeautifulSoup4 |

## 核心功能

### 1. AI 简历解析

一键从招聘网站候选页提取信息，采用「DOM 提取 + LLM 结构化」混合方案：

```
页面 DOM → Site Adapter（CSS 选择器）→ 原始文本 → DeepSeek LLM → 结构化 JSON
```

**输出字段：** 姓名、工作经历（公司/职位/时长/描述）、教育背景（学校/学历/专业）、技能标签、语言能力、薪资期望、所在城市、个人总结。

### 2. 人岗匹配评估

在侧边栏粘贴岗位 JD，AI 一键评估候选人与岗位的匹配度。

**评估输出：**
- **综合匹配分** (0-100)，环形进度图展示
- **五维雷达图**（技术技能、工作经验、学历背景、薪资匹配、综合素养）
- **技能缺口表**，标注匹配/缺失技能
- **推荐等级**（强烈推荐 / 推荐 / 可考虑 / 不推荐）

### 3. 智能话术生成

根据候选人背景和岗位要求，一键生成个性化沟通话术。

**模板类型：** 面试邀请、跟进消息、婉拒信、自定义。

### 4. 数据看板

会话级别的数据统计，包含解析/匹配/消息数量、平均匹配度、每日趋势柱状图、最近活动时间线。

### 5. Selenium 自动化

独立的 Python 自动化脚本，演示浏览器自动数据采集能力。

---

## 项目结构

```
anyjob-hr-copilot/
├── extension/                           # Chrome 插件 (Vue3 + Vite + TS)
│   ├── manifest.json                    # MV3 清单文件
│   ├── vite.config.ts                   # 多入口构建配置
│   ├── src/
│   │   ├── background/
│   │   │   └── service-worker.ts        # Service Worker
│   │   ├── content/
│   │   │   ├── index.ts                 # Content Script 入口
│   │   │   ├── dom-extractor.ts         # 通用 DOM 文本提取
│   │   │   ├── sidebar-injector.ts      # 浮动按钮 + Shadow DOM 隔离
│   │   │   └── site-adapters/           # 各平台 CSS 选择器适配
│   │   │       ├── base.adapter.ts      # 抽象基类
│   │   │       ├── bosszhipin.adapter.ts # BOSS直聘适配器
│   │   │       ├── liepin.adapter.ts    # 猎聘适配器
│   │   │       ├── zhaopin.adapter.ts   # 智联招聘适配器
│   │   │       ├── local.adapter.ts     # 本地测试适配器
│   │   │       └── index.ts             # 适配器注册中心
│   │   └── sidepanel/                   # Vue3 侧边栏应用
│   │       ├── main.ts                  # Vue 应用入口
│   │       ├── App.vue                  # 根布局组件
│   │       ├── router.ts                # Hash 路由
│   │       ├── stores/                  # Pinia 状态管理
│   │       │   ├── candidate.store.ts   # 候选人数据状态
│   │       │   ├── settings.store.ts    # API 配置、已保存 JD
│   │       │   └── history.store.ts     # 浏览历史记录
│   │       ├── composables/
│   │       │   ├── useApi.ts            # 后端 HTTP 请求封装
│   │       │   └── useDomBridge.ts      # Content Script 消息桥接
│   │       ├── pages/
│   │       │   ├── ResumePage.vue       # 标签1: 简历解析
│   │       │   ├── MatchingPage.vue     # 标签2: 人岗匹配 + 雷达图
│   │       │   ├── MessagePage.vue      # 标签3: 智能消息生成
│   │       │   └── DashboardPage.vue    # 标签4: 数据看板
│   │       ├── components/
│   │       │   ├── layout/              # SidebarHeader, SidebarTabs
│   │       │   ├── resume/              # ResumeStructured, ResumeEditForm
│   │       │   ├── matching/            # MatchingScore, RadarChart, SkillGapTable
│   │       │   ├── dashboard/           # StatCard
│   │       │   └── shared/              # LoadingSpinner, ErrorAlert, EmptyState
│   │       └── types/                   # TypeScript 类型定义
│   └── public/icons/
│
├── backend/                             # FastAPI 后端
│   ├── requirements.txt
│   ├── .env.example
│   ├── app/
│   │   ├── main.py                      # FastAPI 入口 + CORS
│   │   ├── config.py                    # 配置管理
│   │   ├── routes/                      # API 路由
│   │   │   ├── health.py                # GET  /api/health
│   │   │   ├── resume.py                # POST /api/resume/parse
│   │   │   ├── matching.py              # POST /api/matching/score
│   │   │   ├── message.py               # POST /api/message/generate
│   │   │   └── dashboard.py             # GET  /api/dashboard/stats
│   │   ├── services/                    # 业务逻辑
│   │   │   ├── llm_client.py            # DeepSeek API 封装 + Mock 模式
│   │   │   ├── resume_parser.py         # 提示词 → JSON → Candidate
│   │   │   ├── matcher.py               # 候选人 + JD → 匹配评估
│   │   │   └── message_generator.py     # 上下文 → 沟通话术
│   │   ├── models/                      # Pydantic v2 数据模型
│   │   │   ├── candidate.py             # 候选人模型
│   │   │   ├── matching.py              # 匹配结果模型
│   │   │   ├── message.py               # 消息请求/响应模型
│   │   │   └── dashboard.py             # 看板统计模型
│   │   ├── prompts/                     # LLM 提示词模板
│   │   │   ├── resume_parse.py          # 简历解析提示词
│   │   │   ├── matching.py              # 人岗匹配提示词
│   │   │   └── message.py               # 话术生成提示词
│   │   └── store/
│   │       └── memory_store.py          # 内存会话数据聚合
│   └── scripts/
│       ├── test_e2e.py                  # 端到端管线测试
│       ├── test_candidate.html          # 本地演示用测试页面
│       └── selenium_demo.py             # Selenium 自动化演示
│
└── docs/
```

---

## 快速开始

### 环境要求

- Node.js 18+, npm
- Python 3.10+ (推荐 conda)
- Chrome 浏览器

### 1. 安装依赖

```bash
# 前端
cd anyjob-hr-copilot
npm install

# 后端
conda activate Ai   # 或你的 Python 环境
pip install -r backend/requirements.txt
```

### 2. 配置 API Key

```bash
# 编辑 backend/.env
DEEPSEEK_API_KEY=sk-你的真实Key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

**Mock 模式：** 如果 API Key 以 `sk-test-` 开头，后端自动使用内置 mock 数据，无需真实 API Key 即可离线演示。

### 3. 启动后端

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

验证：`curl http://localhost:8000/api/health` → `{"status":"ok","model":"deepseek-chat"}`

### 4. 运行管线测试

```bash
python backend/scripts/test_e2e.py
# 预期输出：5 passed, 0 failed
```

### 5. 构建并加载插件

```bash
npm run build:extension
```

1. Chrome → `chrome://extensions`
2. 开启右上角 **开发者模式**
3. 点击 **加载已解压的扩展程序**
4. 选择 `extension/dist/` 文件夹

---

## 实机演示指南

### 启动测试页面

```bash
cd backend/scripts
python -m http.server 8080
```

在 Chrome 中打开 `http://localhost:8080/test_candidate.html`

### 演示流程

| 步骤 | 操作 | 展示要点 |
|------|------|---------|
| 1 | 打开测试页面，点击右下角浮动 **🤖 AI 解析** 按钮 | Content Script 注入成功，侧边栏打开 |
| 2 | **简历解析** 标签：点击 **🔍 提取页面简历** | 结构化简历展示：姓名、技能云、工作经历、教育背景 |
| 3 | **人岗匹配** 标签：粘贴 JD，点击 **🎯 开始匹配** | 环形评分图 + ECharts 雷达图 + 技能缺口表 |
| 4 | **智能消息** 标签：选择模板，点击 **✨ 生成消息** | 个性化沟通话术，一键复制 |
| 5 | **数据看板** 标签 | 4 个统计卡片 + 每日趋势图 + 活动时间线 |

---

## API 接口文档

### `GET /api/health`

健康检查，返回当前模型信息。

**响应：**
```json
{"status": "ok", "model": "deepseek-chat"}
```

### `POST /api/resume/parse`

将原始简历文本解析为结构化数据。

**请求：**
```json
{
  "raw_text": "张小明 男 28岁 本科 5年经验\n工作经历：字节跳动 高级前端...",
  "source_site": "zhipin.com"
}
```

**响应：**
```json
{
  "name": "张小明",
  "years_of_experience": 5,
  "current_title": "高级前端开发工程师",
  "current_company": "字节跳动",
  "skills": ["Vue3", "TypeScript", "React", "JavaScript"],
  "education": [{"school": "上海交通大学", "degree": "本科", "major": "计算机科学与技术"}],
  "work_experience": [{"company": "字节跳动", "title": "高级前端开发工程师", "duration_months": 36}],
  "summary": "5年前端开发经验，精通Vue3和React..."
}
```

### `POST /api/matching/score`

评估候选人与岗位的匹配度。

**请求：**
```json
{
  "candidate": { /* /resume/parse 返回的 Candidate 对象 */ },
  "jd_text": "高级前端开发工程师\n要求：3年以上前端经验..."
}
```

**响应：**
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
  "weaknesses": ["后端技术储备不足"]
}
```

### `POST /api/message/generate`

生成个性化沟通话术。

**请求：**
```json
{
  "candidate": { /* Candidate 对象 */ },
  "jd_title": "高级前端开发工程师",
  "jd_company": "字节跳动",
  "template_type": "面试邀请",
  "custom_instruction": ""
}
```

**响应：**
```json
{
  "message": "张小明确认好！\n\n我是AnyJob平台的HR，仔细看了你的简历...",
  "template_used": "面试邀请",
  "tokens_used": 0
}
```

### `GET /api/dashboard/stats?days=7`

获取会话统计数据。

**响应：**
```json
{
  "total_parsed": 5,
  "total_matched": 3,
  "total_messages": 2,
  "avg_match_score": 82.5,
  "daily_breakdown": [{"date": "2026-05-29", "parsed_count": 5, "matched_count": 3, "message_count": 2}],
  "recent_activity": [{"timestamp": "...", "action": "简历解析", "candidate_name": "张小明", "detail": "成功解析"}]
}
```

---

## 扩展新平台

新增一个招聘网站只需**一个适配器文件**（约 50 行代码）：

1. 创建 `extension/src/content/site-adapters/newsite.adapter.ts`
2. 继承 `BaseSiteAdapter`，用 CSS 选择器实现 `extractAll()` 方法
3. 在 `site-adapters/index.ts` 注册一行
4. 在 `manifest.json` 的 `host_permissions` 添加域名

后续的 LLM 解析、匹配评估、话术生成完全复用。

```typescript
// 示例：新增平台适配器
export class NewSiteAdapter extends BaseSiteAdapter {
  name = 'newsite.com'

  extractAll(): Record<string, string> {
    return {
      name:             this.text('.candidate-name'),
      basicInfo:        this.textAll('.info-item span'),
      workExperience:   this.textAll('.experience-section'),
      skills:           this.list('.skill-tag'),
      education:        this.text('.education-section'),
      selfDescription:  this.text('.summary'),
      salaryExpectation: this.text('.salary'),
    }
  }
}
```

---

## 面试展示要点

- **架构设计**：Content Script → Service Worker → Side Panel 三层通信，消息类型安全
- **设计模式**：Site Adapter 符合开闭原则，新增平台不改现有代码
- **提示词工程**：迭代优化 LLM 提示词，解析准确率 90%+
- **样式隔离**：Shadow DOM 确保插件样式不污染宿主页面
- **Mock 模式**：`sk-test-` 前缀自动切换离线演示，体现测试策略
- **模块化设计**：每个 AI 能力（解析/匹配/话术）独立服务 + 独立提示词模板

---

## License

MIT
