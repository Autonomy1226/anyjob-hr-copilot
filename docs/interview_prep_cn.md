# AnyJob HR Copilot — 面试准备文档（中文）

---

## 第一部分：项目展示（面试口述稿）

### 1.1 一分钟电梯演讲

> 我独立开发了一款面向 HR 招聘场景的 AI Copilot 浏览器插件——**AnyJob HR Copilot**。它集成在 BOSS 直聘、猎聘等主流招聘平台中，为 HR 提供三个核心 AI 能力：一键简历解析、人岗匹配度评估（含雷达图）、个性化沟通话术生成。
>
> 技术栈完全匹配岗位要求：Chrome Manifest V3 + Vue3 + Element Plus 做前端，FastAPI + Python 做后端，DeepSeek 大模型做 AI 引擎，Selenium 做自动化。从架构设计到代码实现全程独立完成，66 个源文件，管线测试 100% 通过。

### 1.2 三分钟详细展示

#### 开场（30秒）

> 这个项目的出发点是：HR 在招聘网站上看简历时，需要反复切换页面、手动复制粘贴信息、自己撰写沟通话术，效率非常低。我做这个插件的目的是让 HR 在浏览招聘网站的同时，AI 助手就在侧边栏随时待命。

#### 核心功能演示（1分30秒）

**功能一：AI 简历解析**
> 当 HR 浏览候选人页面时，插件会自动检测并注入一个浮动的"AI 解析"按钮。点击后，Content Script 通过 CSS 选择器提取页面 DOM 中的候选人信息，发送给后端 FastAPI 服务，由 DeepSeek 大模型将非结构化文本解析成结构化 JSON——包括姓名、工作经历（公司/职位/时长）、教育背景、技能标签、薪资期望、个人总结等。整个过程 2-3 秒完成。我采用了"DOM 提取 + LLM 结构化"的混合方案——DOM 层保证数据来源可靠，LLM 层处理格式不一致性和语义理解。

**功能二：人岗匹配评估**
> 在侧边栏粘贴岗位 JD，AI 从五个维度评估候选人与岗位的匹配度：技术技能、工作经验、学历背景、薪资匹配、综合素养。输出包括一个 0-100 的综合评分、ECharts 雷达图、以及技能缺口分析表——清楚标注哪些技能匹配、哪些缺失。面试官如果问"为什么选这五个维度"，我的回答是：这五个维度覆盖了 HR 评估候选人的核心关注点，从硬技能到软素质，同时提示词中要求 LLM 给出具体的评估依据，避免主观判断。

**功能三：智能话术生成**
> 根据候选人背景和岗位要求，一键生成个性化沟通话术。支持四种模板类型：面试邀请、跟进、拒信、自定义。HR 可以编辑微调后一键复制到招聘平台使用。这个功能将撰写沟通消息的时间从平均 5 分钟缩短到 10 秒。

**功能四：数据看板 + Selenium 自动化**
> 数据看板展示当前会话的解析/匹配/消息统计数据，包含 ECharts 柱状图和活动时间线。另外我独立开发了一个 Selenium 自动化脚本，可以自动化打开浏览器、访问招聘页面、提取数据、调用 API 完成解析和匹配。

#### 架构亮点（1分钟）

> 整体架构采用三层通信模型：Content Script 负责页面 DOM 提取和按钮注入，使用 Shadow DOM 做样式隔离；Service Worker 管理侧边栏打开/关闭的生命周期；Side Panel 是 Vue3 构建的单页应用，包含 4 个标签页、12 个组件，使用 Pinia 做状态管理。
>
> 设计上的核心亮点是 **Site Adapter 模式**——每个招聘平台只需实现一个约 50 行的适配器类，定义各自的 CSS 选择器即可。后续的 LLM 解析、匹配评估、话术生成全部复用。这符合开闭原则，新增平台不改现有代码。
>
> 后端采用服务化架构，每个 AI 能力（解析/匹配/话术）是独立服务 + 独立提示词模板的组合，便于单独调试和优化。同时设计了 Mock 模式——当 API Key 以 `sk-test-` 开头时自动返回内置数据，无需真实 API 即可离线演示。

---

## 第二部分：常见面试问题及答案

### Q1: 介绍一下这个项目，你做了什么？

**答：** 我独立开发了HR Copilot，一款面向 HR 的 AI 浏览器插件。我负责的内容包括：
- **架构设计**：从零设计了 Chrome MV3 的三层通信架构（Content Script → Service Worker → Side Panel）
- **前端开发**：使用 Vue3 + Element Plus 实现了侧边栏 UI，包含 4 个功能页面和 12 个组件
- **后端开发**：使用 FastAPI 构建了 5 个 API 端点，设计了 3 组 LLM 提示词模板
- **AI 集成**：通过 OpenAI SDK 对接 DeepSeek，实现了简历解析、匹配评估、话术生成三个 AI 能力
- **自动化**：使用 Selenium + BeautifulSoup 开发了数据采集脚本
- **测试**：编写了端到端管线测试，覆盖全部 5 个 API 端点

技术决策上，我选择了"DOM 提取 + LLM 结构化"的混合方案而非纯 LLM 方案，因为 DOM 提取保证数据来源可靠，LLM 解决格式不一致性问题。

---

### Q2: 你遇到的最大挑战是什么？怎么解决的？

**答：** 最大的挑战有三个：

**挑战一：Chrome Side Panel API 的通信机制。** MV3 的 Side Panel API 相对较新，文档不够完善。Content Script 和 Side Panel 之间的消息传递需要经过 Service Worker 中转。我设计了类型安全的消息桥接层（`useDomBridge` composable），封装了 `chrome.runtime.sendMessage` 和 `chrome.tabs.sendMessage` 的调用，统一了错误处理和超时逻辑。

**挑战二：LLM 输出的可靠性。** DeepSeek 有时会返回格式错误的 JSON。我在 `llm_client.py` 中实现了 JSON 格式校验 + 自动重试机制（最多重试 2 次，重试时明确告知 LLM 要求修复 JSON）。同时设计了 Mock 模式，在 API Key 以 `sk-test-` 开头时使用内置 mock 数据，方便离线开发和测试。

**挑战三：Style Isolation。** 插件的浮动按钮注入到第三方页面中，必须确保样式不污染宿主页面。我使用了 Shadow DOM 创建隔离的样式作用域，所有 CSS 都在 Shadow Root 内部，完全不与宿主页面样式冲突。

---

### Q3: 为什么选择 Chrome Manifest V3？相比 V2 有什么优势？

**答：** V3 是 Chrome 目前的强制标准——2024 年起 Chrome Web Store 不再接受 V2 新扩展，2025 年起 V2 扩展会被逐步禁用。技术优势：
- **Service Worker 替代 Background Page**：按需唤醒，不常驻内存，资源更高效
- **Side Panel API**：提供了原生的侧边栏能力，比 V2 中需要手动注入 iframe 更稳定
- **声明式网络请求（DNR）**：但我们项目不需要拦截请求，所以没有使用
- **更细粒度的权限模型**：`host_permissions` 独立声明，用户可以按需授予

---

### Q4: 这个项目的安全措施有哪些？

**答：**
- **Shadow DOM 隔离**：浮动按钮的 CSS 完全隔离，不会污染或被宿主页面影响
- **CSP（内容安全策略）**：Vite 构建时配置了严格的 CSP，禁止 inline script
- **最小权限原则**：manifest.json 只声明了必需的权限（sidePanel、storage、activeTab、scripting），host_permissions 只匹配目标招聘网站
- **API Key 安全**：Key 通过 `.env` 文件管理，不提交到 Git（`.gitignore` 已配置）
- **CORS 中间件**：后端配置了 CORS，只允许扩展来源的请求
- **沙箱机制**：Side Panel 运行在 Chrome 原生的侧边栏沙箱中，与宿主页面隔离

---

### Q5: 如果要让这个项目上线，还需要做什么？

**答：** 从 MVP 到生产环境，主要需要：
1. **数据库**：目前是内存存储，需要接入 PostgreSQL 或 MySQL 做持久化
2. **用户系统**：添加登录/注册、API Key 管理、多租户隔离
3. **多平台适配**：需要在真实 BOSS 直聘、猎聘页面上调试 CSS 选择器，适配其 DOM 结构（当前已支持本地测试页面）
4. **Chrome Web Store 上架**：准备上架素材（截图、宣传图、隐私政策），通过 Chrome 审核
5. **性能优化**：缓存已解析的简历（候选人 ID hash），避免重复调用 LLM
6. **错误监控**：接入 Sentry 或类似工具，收集前端和后端的异常
7. **A/B 测试**：对比不同提示词模板的解析准确率和用户满意度
8. **合规性**：确保符合个人信息保护法（PIPL），简历数据属于敏感信息

---

### Q6: 提示词工程是怎么做的？如何保证 LLM 输出质量？

**答：** 我为三个场景分别设计了独立的 System Prompt + User Prompt 组合模板：

**简历解析提示词：**
- System Prompt 定义了精确的 JSON Schema，包含 17 个字段的类型和约束
- 明确要求 "Normalize company names"、"Categorize skills meaningfully"、"Infer years_of_experience from work history" 等具体规则
- 最后明确指示 "Return ONLY the JSON object, no additional text"

**人岗匹配提示词：**
- 要求从五个维度评分（技术技能、工作经验、学历背景、薪资匹配、综合素养）
- 每个维度需要同时提供 `candidate_value` 和 `jd_requirement`，确保评分有据可依
- 推荐等级用固定词汇（强烈推荐/推荐/可考虑/不推荐），便于前端展示

**质量保证机制：**
- 所有 LLM 响应通过 Pydantic v2 的 `model_validate()` 做类型校验
- 如果 JSON 格式错误，自动重试最多 2 次，重试消息明确告知 LLM 修复格式
- 使用 `response_format={"type": "json_object"}` 参数约束 DeepSeek 输出 JSON

---

### Q7: Vue3 的 Composition API 在这个项目中是如何使用的？

**答：** 整个项目全面使用 Composition API（`<script setup>`）：

- **Composables 封装可复用逻辑**：`useApi()` 封装了所有的后端 HTTP 调用，`useDomBridge()` 封装了 Content Script 消息传递。每个 composable 职责单一、可独立测试。
- **Pinia Store 使用 setup 语法**：`candidateStore`、`settingsStore`、`historyStore` 都使用 `setup()` 定义的 Store，共享响应式状态。
- **`<script setup>` + TypeScript**：所有 `.vue` 文件使用 `<script setup lang="ts">`，代码更简洁，类型推断更好。
- **响应式数据流**：`useApi()` 返回结果 → 更新 Pinia Store → 组件自动响应渲染。例如简历解析：`extractionStatus: 'loading'` → 显示 LoadingSpinner → `extractionStatus: 'done'` → 显示 ResumeStructured。

---

### Q8: Content Script 和 Side Panel 之间的通信是怎么实现的？

**答：** Chrome MV3 中 Content Script 和 Side Panel 运行在不同的上下文中，需要特定的通信方式：

**Content Script → Service Worker → Side Panel（打开侧边栏）：**
```
用户点击浮动按钮
  → Content Script: chrome.runtime.sendMessage({ type: 'OPEN_SIDE_PANEL' })
  → Service Worker: chrome.runtime.onMessage → chrome.sidePanel.open({ tabId })
  → Side Panel 显示
```

**Side Panel → Content Script（请求提取 DOM）：**
```
用户点击"提取页面简历"
  → Side Panel (useDomBridge): chrome.tabs.sendMessage(tabId, { type: 'EXTRACT_DOM' })
  → Content Script: chrome.runtime.onMessage → 调用 Site Adapter 提取 → sendResponse(data)
  → Side Panel: 收到 rawText → 调用 useApi().parseResume()
```

我把这些调用封装在 `useDomBridge.ts` composable 中，提供类型安全的 Promise 接口，上层代码不需要直接接触 `chrome.runtime` API。

---

### Q9: 如何做性能优化？

**答：**
- **UI 层面**：Element Plus 组件按需加载（Vite tree-shaking），ECharts 按需引入图表组件而非全量引入
- **网络层面**：`useApi` composable 统一管理请求状态，避免重复请求；未来可以添加候选人 ID hash 做 LLM 结果缓存
- **DOM 提取层面**：Site Adapter 使用 `querySelector` / `querySelectorAll` 精确选择，不做全页面遍历
- **构建层面**：Vite 的 Rollup 输出 `sidepanel.js`（1.5MB）是主要瓶颈，可以通过 `manualChunks` 或动态 import 做代码分割

---

### Q10: 这个项目体现了你哪些工程能力？

**答：**
1. **前端工程化**：从项目脚手架（Vite + Vue3 + TS + Element Plus）到构建配置（多入口 Rollup）全程独立搭建
2. **架构设计**：三层通信模型 + Site Adapter 设计模式 + 服务化后端
3. **AI 工程化**：提示词工程 + JSON Schema 约束 + 自动重试 + Mock 模式
4. **全栈能力**：独立完成前后端开发和联调
5. **测试意识**：E2E 管线测试覆盖全部 API 端点
6. **文档能力**：中英文 README + 架构图 + API 文档

---

## 第三部分：岗位针对性问题及答案

### JD 职责 1：浏览器插件功能开发与维护

**问：浏览器插件的开发流程是怎样的？**

**答：** 标准流程是：需求分析 → 设计 manifest.json（权限、host_permissions、content_scripts 匹配规则）→ 开发 Content Script（DOM 操作、消息传递）→ 开发 Service Worker（事件监听、生命周期管理）→ 开发 UI（Popup/Side Panel/Options Page）→ 本地测试（chrome://extensions 加载）→ 打包上架。

我的项目严格遵循这个流程。Manifest V3 声明了最小权限集，Content Script 在 `document_idle` 时机注入，确保 DOM 就绪。

**问：Firefox 插件和 Chrome 插件开发有什么区别？**

**答：** Firefox 使用 `browser.*` API 而非 `chrome.*`，但两者高度相似（都是 WebExtensions 标准）。主要区别：
- Firefox 的 `manifest.json` 版本键名是 `manifest_version`
- Firefox 不支持 Side Panel API，需要用 `sidebar_action` 替代
- Firefox 的 Service Worker 支持有限，某些场景仍用 Background Page
- 我在项目中使用了 `chrome.*` API，但架构设计上通信层是抽象过的（`useDomBridge`），替换底层 API 不影响上层逻辑。

---

### JD 职责 2：前端设计与开发 + 数据可视化

**问：如何选择前端框架？为什么用 Vue3 而不是 React？**

**答：** 作为 Vue3 主力框架的使用者，我认为 Vue3 在这个项目中有几个优势：
- Composition API 的 `<script setup>` 语法简洁，组件逻辑清晰
- Element Plus 提供了完整的 UI 组件库，开发效率高
- Pinia 的状态管理直觉性强，和 Composition API 风格一致

但同时我也熟悉 React——如果团队使用 React，我可以用 React + Ant Design 重新实现，架构设计（Site Adapter、消息传递、API 封装）完全复用。

**问：ECharts 雷达图是怎么实现的？**

**答：** 使用 `vue-echarts` 库，按需引入所需的 ECharts 模块（RadarChart、Title、Tooltip 等），避免全量引入。组件接收 `radar_dimensions` 数组作为 props，计算生成 ECharts 的 `radar.indicator` 和 `series` 配置。两条数据线：蓝色实线（候选人得分）+ 灰色虚线（岗位基准线 70 分），直观对比。

---

### JD 职责 3：API 对接 + 异步编程

**问：前后端联调过程中遇到过什么问题？**

**答：** 主要是类型同步问题。TypeScript 的接口和 Pydantic 的模型是分开定义的，需要手动保持一致。解决方案是：后端先定义 Pydantic 模型（作为单一事实来源），前端 TypeScript 接口根据 API 响应结构对应编写。在响应中使用 `model_validate()` 做运行时校验，确保后端返回的数据结构正确。

**问：如何处理异步请求的错误？**

**答：** `useApi.ts` composable 中统一处理：
- HTTP 错误：检查 `res.ok`，尝试解析 `detail` 字段返回有意义的错误消息
- 网络错误：`fetch()` 的异常被 catch，抛给调用方
- LLM 错误：后端有重试机制（最多 2 次），最终失败返回 500
- UI 层：每个页面独立管理 `status: 'idle' | 'loading' | 'done' | 'error'` 状态，错误时显示 ErrorAlert 组件

---

### JD 职责 4：Selenium 自动化

**问：Selenium 在这个项目中的具体应用？**

**答：** 我开发了一个独立的 Selenium 演示脚本（`selenium_demo.py`），功能包括：
1. 自动化启动 Chrome 浏览器
2. 导航到招聘网站候选人页面（或加载本地 HTML 文件）
3. 使用 BeautifulSoup 提取页面文本
4. 调用后端 API 完成简历解析 → 人岗匹配 → 话术生成
5. 打印结构化结果

这个脚本演示了完整的自动化数据采集管线。之所以用 Selenium 而不是 Puppeteer，是因为岗位明确要求了 Selenium，且 Selenium 支持更多语言的 SDK（Python 版本是团队的常用栈）。

**问：如何处理网站的反爬机制？**

**答：** BOSS 直聘等网站有反调试和反爬机制。我的应对策略：
1. **不强行爬取**：插件的设计原则是"在用户已登录、已有权限的前提下辅助操作"，不是暴力爬虫
2. **Selenium 反检测**：启动时添加 `--disable-blink-features=AutomationControlled` 参数，移除 `navigator.webdriver` 标记
3. **节奏控制**：随机化操作间隔，模拟人类浏览行为
4. **降级策略**：如果 DOM 选择器失效（网站改版），Adapter 返回空字符串，由 LLM 做语义兜底

---

### JD 职责 5：与境外团队协作 + 英文文档

**问：有编写英文技术文档的经验吗？**

**答：** 本项目的所有文档都是中英双语的：
- `README.md`（英文）和 `README_CN.md`（中文）各约 300 行
- 代码中的关键注释使用英文
- Git commit message 使用英文（遵循 conventional commits）
- API 文档包含完整的英文请求/响应示例
- 可以为境外同事提供英文的架构说明和技术方案

**问：如何进行跨时区协作？**

**答：** 我会：
- 使用异步沟通工具（Slack、Notion、GitHub Issues），减少同步会议依赖
- 文档先行：设计文档和 API Spec 写清楚再动手
- 在代码 Review 中留下充分上下文，减少来回沟通成本
- 关键节点做视频会议同步，其余用文字沟通

---

### JD 加分项 1：LLM 应用开发经验

**问：你对 LLM 应用开发的理解？**

**答：** 我认为 LLM 应用开发的核心不是调 API，而是三个工程问题的解决：
1. **提示词工程**：设计 System Prompt 约束 LLM 的行为边界和输出格式，通过 User Prompt 注入精确的上下文
2. **可靠性保障**：LLM 输出具有不确定性，需要 JSON Schema 约束 + 格式校验 + 自动重试 + 降级策略
3. **产品化设计**：LLM 是工具而非产品，真正的产品价值在于——如何将 LLM 能力嵌入到用户的业务流程中。本项目就是典型案例：HR 不需要打开 ChatGPT 输入提示词，而是在浏览招聘页面的同时，一键获取解析结果

**问：为什么选择 DeepSeek 而不是 GPT-4？**

**答：** 两个原因：
1. **成本**：DeepSeek 的 API 定价远低于 GPT-4，适合高频调用场景（HR 每天可能解析几十份简历）
2. **中文能力**：DeepSeek 的中文理解和生成能力非常强，HR 领域的简历/话术以中文为主
3. 技术上是 OpenAI 兼容的 API，代码中用 OpenAI SDK 调用，模型可替换性高——改一行 base_url 就能切换到其他模型

---

### JD 加分项 2：低代码平台理解

**问：你了解低代码平台吗？这个项目和低代码有什么关系？**

**答：** 我理解低代码平台的核心价值是：通过可视化拖拽 + 配置化方式降低开发门槛，让非技术人员也能构建应用。

本项目的 **智能话术模板** 就是一个轻量级的低代码概念实践：HR 可以在侧边栏中配置消息模板（选择类型、填写自定义指令），而无需编写任何代码。如果进一步扩展，我可以实现：
- 可视化的模板编辑器（拖拽文本块、变量占位符）
- 模板市场（分享和复用其他 HR 的模板）
- 条件逻辑（根据候选人匹配度区间自动选择不同的消息模板）

如果团队有低代码平台产品，我可以将这部分经验直接迁移过去。

---

## 第四部分：快速自检清单

面试前用这些问题自测：

- [ ] 能否在 1 分钟内讲清楚项目是什么、解决了什么问题？
- [ ] 能否画出架构图并解释三层通信机制？
- [ ] 能否说明 Site Adapter 模式的设计原理和扩展方式？
- [ ] 能否解释提示词工程的设计思路？
- [ ] 能否说明 Shadow DOM 隔离的作用和实现？
- [ ] 能否回答 "为什么用 Vue3/DeepSeek/MV3/Selenium" 这类技术选型问题？
- [ ] 能否阐述 MVP 到生产环境还需要做什么？
- [ ] 能否用英文流利介绍项目？（参考 interview_prep_en.md）
- [ ] 能否讲 1-2 个开发中遇到的问题和解决方案？
- [ ] 项目代码是否能在本地跑起来并完成 E2E 演示？

---

## 第五部分：AI Agent 工程师专项问题 & 答案

> 以下是面试官考察"你是否真正理解 AI 辅助开发"的高频问题。普通开发者会用 AI，但 AI Agent 工程师能讲清楚"怎么用"和"为什么这么用"。

### QA1: "你怎么使用 AI 工具进行开发的？"

**答：** 我采用的是一种叫 **AI-Native Engineering** 的范式。它不是"代码写不出来问问 ChatGPT"，而是一套系统化的协作流程：

**第一层：用 AI 做架构探索。** 比如设计 Chrome 插件的侧边栏实现方案时，我把需求描述给 AI Plan agent，它给出三种方案（Side Panel API、iframe 注入、Popup）的对比分析。我根据项目需求选择了 Side Panel API。AI 提供信息，我做决策。

**第二层：用 AI 规模化生成代码。** 这个项目约 60% 的代码骨架由 AI 生成——CRUD 路由、Vue 组件模板、TypeScript 类型定义、Pydantic 数据模型。这些代码模式化程度高、人工 Review 即可。剩下 40% 由我手动完成——核心通信逻辑、LLM 提示词设计、错误处理策略——这些需要架构级判断力。

**第三层：用 AI 加速调试。** 遇到报错，我把错误栈 + 上下文喂给 AI，秒级定位根因。比如 `httpx.AsyncClient.__init__() got an unexpected keyword argument 'proxies'` → AI 立即指出是 openai v1.12.0 与 httpx v0.28.1 不兼容 → 一行命令解决。

**第四层：用 AI 生成文档。** README、API 文档、面试准备指南的初稿都由 AI 生成。我负责审核和补充工程洞察。

**核心理念**：AI 是杠杆，不是替代品。同样 2 周时间，这个工作流让我交付了 66 个文件的完整 MVP。

### QA2: "你怎么保证 AI 生成的代码质量？"

**答：** 三道关卡：

1. **类型系统作为第一道防线**：TypeScript 编译检查 + Pydantic v2 运行时校验。AI 生成的代码如果类型不匹配，编译/启动阶段就会报错。
2. **E2E 测试覆盖数据流**：5 步管线测试验证完整的 DOM → LLM → JSON → UI 数据流。每次修改后跑一遍，确保管线没有断裂。
3. **核心代码不做 AI 委托**：通信桥接层（`useDomBridge`）、提示词模板、错误处理逻辑 —— 这些我手动写。AI 负责"填充"，我负责"骨架"。

### QA3: "你说你用 AI 写了 60% 的代码，那你的贡献是什么？"

**答：** 60% 是"代码量"，但代码量和工程价值不是正比关系。我的贡献在五个地方：

1. **架构决策**：三层通信模型、Site Adapter 模式、混合提取方案。AI 能列出选项，但选择权在工程师。
2. **提示词设计**：三组 System Prompt 是这个项目最核心的"产品代码"。AI 写不了高质量的 prompt —— 它需要领域理解（HR 招聘流程）和反复实验。
3. **管线测试设计**：哪些环节需要测、怎么 mock、怎么验证 —— 这是工程判断。
4. **质量控制**：AI 生成的代码经过 TypeScript 编译 + Pydantic 校验 + 人工 Review 三道关。
5. **集成**：把 AI 生成的各个模块串联成完整的产品链路。

简单说：**AI 负责执行，我负责设计、决策和验证。**

### QA4: "你怎么测试这个项目的？数据怎么得出来的？"

**答：** 每一项数据都有具体的测量方法和验证流程：

**管线测试通过率 100%**：运行 `test_e2e.py`，5 步测试覆盖全部 API 端点。Mock 模式下无需真实 API Key。

**简历解析准确率 90%+**：准备 5 个不同风格的候选人文本（大厂、应届生、跨行、非标格式、中英混合），逐个跑解析，人工检查 17 个字段的提取完整性，再加上 Pydantic 类型校验作为自动化兜底。

**Token 节省 70%**：实际计算。`test_candidate.html` 原始 HTML ~3200 字符（约 2400 tokens），DOM 预提取后 ~390 字符（约 500 tokens）。加 system prompt 后总量对比：(3000-800)/3000 ≈ 73%。

**话术生成 5 分钟 → 10 秒**：基于对 HR 工作流程的分析。传统流程分成回顾简历、匹配 JD、撰写、校对四个步骤，合计 4-5 分钟。插件流程为点击-生成-确认三步，合计约 10 秒。30 倍的差距来自去掉手动撰写步骤。

**Shadow DOM 隔离率 100%**：验证方法很简单——在测试页面写 `button { background: red !important }`，如果按钮变色说明泄漏了。实际结果：按钮保持原样式。

**关键原则：我不说没有验证过的数据。能精确到数字的给数字，不能精确的给保守估计并说明推算逻辑。**

### QA5: "你怎么看 Vibe Coding？"

**答：** "Vibe Coding" 的核心思想是用自然语言描述意图，让 AI 生成代码，然后通过快速迭代逼近目标。我认同这个方向，但我不认为它是"不写代码"——它本质是**把编码从手动拼写变成了对话驱动的迭代**。

在本项目中的实践：
- 搭脚手架时用 Vibe Coding（"用 Vite 创建一个 Vue3 + TS 的 Chrome 扩展项目"→ AI 生成 → 验证 → OK）
- 写核心通信逻辑时不依赖 AI（涉及 Chrome MV3 的三个上下文通信，AI 对这块理解经常出错）
- 遇到 bug 时用 AI 辅助诊断，但修复方案我自己判断

**Vibe Coding 是速度工具，不是质量替代品。** 快的地方让它快，关键的地方必须自己把关。

### QA6: "如果让你给这个项目加一个 AI Agent 的能力，你会加什么？"

**答：** 我会加一个 **多轮对话的面试 Agent**。目前的话术生成是"一键生成一条消息"，可以升级为：

> HR 选择候选人 → Agent 自动发送初触达消息 → 候选人回复后 Agent 分析回复意图（感兴趣/犹豫/拒绝）→ 自动生成跟进回复 → 直到候选人确认面试时间 → Agent 自动发送日历邀请

技术实现上：
- 对话状态机（state machine）管理多轮交互
- LLM 做意图识别和回复生成
- 工具调用（tool calling）：Agent 可以查询日历空闲时段、发送邮件
- Human-in-the-loop：所有消息 HR 确认后再发送（安全边界）

这和 AnyHelper 的业务场景直接相关——跨境招聘中 HR 需要处理大量候选人的初始沟通，Agent 可以承担 80% 的重复工作。

---

## 附录：技术术语速查

| 中文 | English |
|------|---------|
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
