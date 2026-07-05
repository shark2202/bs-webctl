---
type: Specification
title: "Agent-SE 执行规范"
description: "AI-agent 软件工程执行规范：ADR/PRD三问/BDD/Hook→CI→Linter 闭环 + ADR 状态机 + 组件接口表，把文档变成提交闸门拦得住的执行契约。本规范为执行规范，与 Arcadia-SPEC.md（参考概念）并列。"
tags: [agent-se, adr, prd, bdd, ci, linter, specification, execution]
timestamp: 2025-07-05T00:00:00Z
---

# Agent-SE 执行规范 (Agent-SE-SPEC)

**Version 0.1 — Draft**

> 定位声明：
> - [`Arcadia-SPEC.md`](./Arcadia-SPEC.md) = **参考概念**（descriptive）：讲方法论
>   的骨架与概念词典，描述"对的样子长什么样"。
> - 本规范 `Agent-SE-SPEC.md` = **执行规范**（prescriptive）：讲拿什么文件、在哪道
>   闸、用什么模板把概念落地为 agent 绕不过的契约。
> 二者关系：Arcadia 提供 *what & why*，本规范提供 *how & where*。常规软件只读本
> 规范即可；复杂多约束系统回查 Arcadia 补 LA/PA 概念。

---

## 1. 元原理：文档即压缩不变量

AI-agent 单 session 经历 20–50 次上下文压缩。**重要的东西能保留，靠的不是 agent
记忆，是 agent 压缩后重新读取的外部不变量**。这倒过来定义了全部工件的设计目标：

- 必须**短、结构化、可 grep**——压缩后 agent 不会重读 50 页架构书，但会 `rg ADR-`。
- 必须**带状态字段**——压缩后 agent 不能读到已被反转的旧决策还理直气壮。
- 必须**可执行或可机检**——不能只靠人 review 兜底。
- 必须**在提交闸门被强制**——不能停留在"应该读"。

一句话：**文档不是给当前 turn 的辅助，是给压缩后那个 turn 的不变量**。

---

## 2. 四件武器 + 两个补丁

### 2.1 ADR（架构决策记录）——记"为什么"

- 记单点技术决策的 **Context / Decision / Alternatives / Consequences**。
- 一条 ADR = 一个"为什么这么定"。50+ 条 ADR 可定义整个产品架构。
- **linter 强制**：触及"决策性"文件的提交必须引用一条 `accepted` 状态的 ADR；
  违规时拒绝信息里带 ADR 文件链接，agent 自行补齐后再提交。
- 对位 Arcadia：= justification link 的文本化、agent 原生形态（替代 Capella 二进制
  模型链接）。对位 AGENTS.md：= 灵魂 9 决策溯源义务的**工件格式**。

### 2.2 PRD（产品需求文档）——只记三件事

1. **为什么存在**（存在理由，一句话）
2. **解决什么问题**（没有它时的痛）
3. **用户怎么走**（编号用户路径——这也是 BDD 场景的源头）

- 目标函数是"**6 周后的你（或压缩后的 agent）还能读懂**"，不是"完整性"。
- 三问封顶：越长越不能在压缩后存活。
- 对位 Arcadia：= OA 运行分析砍到 3 问（5 步→3 问）。对位 AGENTS.md：= "定好目标
  再跑"+ 灵魂 1 先定义度量的**量化形态**。

### 2.3 BDD + Cucumber——spec 即 test

- 用 Gherkin（Given/When/Then）人类语言描述行为，同时是 CI 可执行测试。
- 核心价值：**读 AI 写的测试比读 AI 写的代码更难**——BDD 让断言本身是人类可读
  spec，agent 漂移意图 = 漂移可读行为，可被 review 抓到。
- 闭合"spec 写了但没人验证"的循环：PRD 第 3 问 → `.feature` 场景 → CI 跑。
- 对位 Arcadia：= scenario 驱动 IVVQ 的**可执行形态**（Arcadia 场景只在模型里，不
  跑）。对位 AGENTS.md：= 灵魂 8 可复现验证的**可读升级**（从"有脚本"到"断言即
  spec"）。

### 2.4 闸门闭环：Git Hook → CI → Linter——让问题不可能发生

```
agent 提交 → pre-commit hook 检查 → 拒绝 + 反馈 + 文档链接 → agent 自修 → 再提交
                                                     ↓
                                              CI 跑 BDD/lint → block merge
``- 哲学：不是"发现问题"，是"让问题不可能发生"——shift-left 到 agent 无法提交非合规
  产物的程度。
- 拒绝信息**必须带文档链接**：压缩后 agent 失去对话记忆，但拒绝信息里自带"违反哪
  条"的指针，可自纠。
- 对位 AGENTS.md：= 灵魂 2 门禁 + 原则"验证：自动化流水线不间断校验"的**物理执行
  点**。

### 2.5 补丁 A：ADR 状态机

ADR 必须带状态字段，linter 据此拒绝"引用已废弃决策"：

```
        review            review
proposed ──────▶ accepted ──────▶ deprecated
                     │                  ▲
                     │   new ADR        │ (orphan)
                     ▼   accepted       │
                 superseded ────────────┘
                 (superseded_by: ADR-NNN 必填)
```

- `proposed`：草案，不可被外部引用强制。
- `accepted`：当前生效，**唯一可被提交引用的状态**。
- `deprecated`：失效且无后继（孤儿）。
- `superseded`：被新 ADR 取代，`superseded_by` 必填。
- linter 规则：提交引用的 ADR 状态必须为 `accepted`；引用 `superseded`/`deprecated`
  → 拒绝并指向 `superseded_by` 后继。

### 2.6 补丁 B：组件接口表（LA/PA 轻量替代）

ADR 记单点决策，但不显式表达"组件树 + 接口"。多组件系统需一份组件接口表（markdown
表格即可，**不引入 Capella**）：

| 组件 | 职责 | 对外接口（输入→输出） | 论证 ADR |
|------|------|----------------------|----------|
| `service/auth` | 用户认证与会话 | `login(cred) → Token` | ADR-0042 |
| `service/payment` | 支付编排 | `charge(order) → Receipt` | ADR-0043 |

- 单组件系统可声明豁免（"无组件接口表：单组件"）。
- 对位 Arcadia：= LA/PA 组件分解 + interface 的**文本最小形态**。

---

## 3. 工件格式（模板）

### 3.1 ADR 模板

```markdown
---
adr: ADR-0042
status: accepted          # proposed | accepted | deprecated | superseded
superseded_by: ""         # 仅 status=superseded 时填 ADR-NNN
date: 2025-07-05
tags: [arch, persistence]
---
# ADR-0042: 选择 SQLite 作为本地持久化

## Context
（决策触发点：要调和的力 / 约束 / 场景。为什么现在必须决定。）

## Decision
（选了什么。一句话能说清。）

## Alternatives Considered
- **选项 A** —— 优点 / 缺点 / 为何不选
- **选项 B** —— 优点 / 缺点 / 为何不选

## Consequences
- 正面：…
- 负面：…
- 需后续跟进：…
```

### 3.2 PRD 模板（三问封顶）

```markdown
---
prd: PRD-<slug>
date: 2025-07-05
status: accepted
---
# PRD: <特性名>

## 1. 为什么存在
（一句话存在理由。6 周后你能读懂。）

## 2. 解决什么问题
（没有它时用户的痛 / 工程的痛。）

## 3. 用户怎么走
1. …
2. …
3. …
（编号路径。每条可映射为一个 BDD 场景。）
```

### 3.3 BDD feature 模板

```gherkin
Feature: 用户登录后会话保持有效
  作为用户
  我想要登录后不必重复登录
  以便顺畅使用服务

  Scenario: 首次登录成功后获得有效会话
    Given 一个已注册用户
    When 该用户提交正确的凭据
    Then 系统返回一个有效会话令牌
```

**step 命名纪律**：step 必须用领域动词表达**意图**，不得镜像实现。
- ✅ `When 该用户提交正确的凭据`
- ❌ `When 调用 AuthApi.login(req) 并点击 id=submit-btn`（含实现词）

### 3.4 组件接口表模板

见 §2.6 表格。多组件系统放 `design/components.md`。

---

## 4. 闸门矩阵

| 闸门 | 触发点 | 检查项 | 失败动作 |
|------|--------|--------|----------|
| **pre-commit hook** | `git commit` | (1) 触及决策性文件的提交引用了 `accepted` ADR；(2) 不引用 `superseded`/`deprecated` ADR；(3) 新增 feature 有 PRD 或显式声明豁免 | reject + 输出违反的文档链接 |
| **CI** | push / PR | (1) BDD `.feature` 全绿；(2) lint 零错；(3) ADR 状态字段合法；(4) 被引用的 ADR 状态 = `accepted` | block merge + 反馈带文档链接 |
| **linter** | 本地 / CI | (1) ADR 模板字段齐全；(2) PRD 含三节；(3) BDD step 名不含实现词（启发式：含 `id=`/`class=`/CSS 选择器/函数名 → 警告） | fail + 指针 |

"决策性文件"的定义由仓库给定（如 `arch/`、`design/**`、接口文件、CI 配置），在
`index.md` 中声明为事实源清单（见 §6）。

---

## 5. 失败模式与防护

| 失败模式 | 表现 | 预防 | 兜底（已发生） |
|----------|------|------|----------------|
| **ADR cargo-cult** | 空壳 ADR 过闸 | linter 查**存在性**；人审**质量**（AGENTS.md 灵魂 3：度量者 ≠ 执行者，两层不可合并） | review 抽样打回；连续空壳 → 触发红线评审 |
| **BDD 镜像实现** | step 名 = `click #submit` | linter 启发式警告；step 强制用领域动词 | 重写 step 为领域动词 |
| **压缩后读陈旧 ADR** | 决策反转但 ADR 未标 `superseded` | ADR 状态机 + `log.md` 时间轴 + linter 拒绝 ref `superseded` | 检索时强制 `rg superseded` 看后继 |

---

## 6. 与 AGENTS.md 的咬合

本规范是 AGENTS.md 哲学的**操作套件**，非竞争关系：

| AGENTS.md 条目 | 本规范提供的落地形态 |
|----------------|---------------------|
| 灵魂 1 先定义度量 | PRD 三问 |
| 灵魂 2 门禁 ≥ 90 | pre-commit hook + CI 闸门矩阵 |
| 灵魂 3 度量者 ≠ 执行者 | linter 查存在性 / 人审质量 的两层分工 |
| 灵魂 8 可复现验证 | BDD（断言即 spec 的可执行验证） |
| 灵魂 9 决策溯源义务 | ADR + 状态机 + `log.md` 时间轴 |
| "过程优于结果" | 强制生成 design/PRD/ADR 工件 |
| "最小代理单元" | PRD/ADR 单文件单决策，极小化上下文 |

**事实源清单**（AGENTS.md 灵魂 9 要求项目记录的跨文件复用值）应在 `index.md` 声明，
至少包括：ADR 目录、PRD 目录、BDD features 目录、组件接口表、闸门配置文件。
修改这些清单项前必须 `rg <关键词> adr/ log.md` 检索历史红线。

---

## 7. 一致性要求（Conformance）

一个仓库**符合本 Agent-SE-SPEC v0.1**，若：

1. **ADR 落地**：有 `adr/` 目录，每条 ADR 遵循 §3.1 模板且状态字段合法；
2. **PRD 落地**：每个 feature 有 §3.2 PRD 或显式声明"无需 PRD"并附理由；
3. **BDD 落地**：行为覆盖由 `.feature` 场景表达且在 CI 执行通过；
4. **闸门落地**：pre-commit hook 与 CI 按 §4 矩阵配置；
5. **状态机落地**：被引用的 ADR 状态均为 `accepted`；`superseded` 必填后继；
6. **时间轴落地**：`log.md` 记录决策反转（ADR 状态迁移）；
7. **组件表落地**：多组件系统有 `design/components.md`；单组件显式豁免。

消费方应将其他约束视为软指导，**不得**因以下情形拒绝：未用的 BDD step 高级写法、
自定义 ADR tag、豁免的组件接口表——只要豁免点与理由被显式记录。

---

# Citations

[1] Michal Cichra（微软/Red Hat 十年老兵）——四个文档武器框架：ADR / PRD 三问 /
    BDD+Cucumber / Git Hook→CI→Linter 闭环；"20–50 次压缩不重要，重要的总会保留"。
    （本规范的源框架，引自当前方法论讨论）

[2] Michael Nygard —— *Documenting Architecture Decisions*（ADR 原始格式，
    Context/Decision/Status/Consequences）。本规范 §3.1 在其基础上增加
    Alternatives 与状态机字段（MADR 风格）。

[3] Cucumber / Gherkin —— *Behavior-Driven Development*（Given/When/Then 可执行
    spec）。本规范 §3.3 增"step 命名纪律：意图非实现"。

[4] 本仓库 [`Arcadia-SPEC.md`](./Arcadia-SPEC.md) ——参考概念侧（need/solution 分层、
    justification link、scenario 驱动 IVVQ、LA/PA 组件分解）。本规范为其概念提供
    agent 原生、可执行、有闸门的落地形态。

[5] 本仓库 [`AGENTS.md`](./AGENTS.md) ——哲学侧（门禁、可复现验证、决策溯源、过程
    优于结果、最小代理单元）。本规范为其条目提供工件格式与执行点。
