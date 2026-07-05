---
type: Specification
title: "Arcadia 方法论规范"
description: "Arcadia（ARChitecture Analysis and Design Integrated Approach）方法论规范：定义基于模型的系统工程五阶段工程视角、核心概念、原则、可追溯性与 Capella 工具映射。"
tags: [mbse, arcadia, capella, systems-engineering, specification]
timestamp: 2025-07-05T00:00:00Z
---

# Arcadia 方法论规范 (Arcadia-SPEC)

**Version 0.1 — Draft**

> Arcadia = **ARChitecture Analysis and Design Integrated Approach**。
> 一种以系统架构为中心、以基于模型的工程活动为基础的系统与软件/硬件架构工程
> 方法，由 Thales 创立，经 Eclipse Foundation（PolarSys）开源，由 Capella 建模
> 工作台实现。本规范来自以下三处权威来源的可复现抓取与整理（见 §Citations）：
> mbse-capella.org/arcadia.html、eclipse.org/capella、uml.org.cn/modeler/202110141.asp。

---

## 1. 定位与目标

Arcadia 是一种**工具化的方法论（tooled method）**， devoted to systems &
architecture engineering，由 Capella 建模工具支撑。它描述了工程推理的细节，
用以：

1. **理解真实的客户需求**（understand the real customer need）；
2. **定义并在所有工程干系人之间共享产品架构**（define and share the product
   architecture among all engineering stakeholders）；
3. **早期验证设计并为其提供论证**（early validate its design and justify it）；
4. **简化并掌控 IVVQ**——Integration、Validation、Verification、Qualification。

**适用对象**：复杂系统、设备、软件或硬件架构定义，尤其是需在强约束间寻求折中
的场景（cost、performance、safety、security、reuse、consumption、weight…）。

**定位金句**：架构是首要的工程驱动因素（*Architecture as prime engineering
driver*）。先做"需要什么"（need），再做"如何实现"（solution）。

---

## 2. 核心原则

| # | 原则 | 含义 |
|---|------|------|
| P1 | **架构即首要工程驱动** | 架构设计先于、并驱动需求落实与实现决策。 |
| P2 | **基于模型的方法** | 所有工程产出沉淀为一个共享模型，而非散落文档。 |
| P3 | **需要导向 vs 解决定向分层** | 上层（OA/SA）描述 *need*，需与客户共同确认；下层（LA/PA/EPBS）描述 *solution*。 |
| P4 | **视角驱动（viewpoint-driven）** | 用 viewpoints 形式化非功能约束（安全、性能、实时、安全保密、可复用、成本、风险…）对架构的影响，并求最佳折中。 |
| P5 | **功能驱动建模** | 以功能与接口为建模主线，需求与功能相联系（区别于 SysML 的需求驱动建模）。 |
| P6 | **抽象层级内置** | 抽象层级是 Arcadia 的 DNA；用层级掩蔽与限制复杂度。 |
| P7 | **可追溯性** | 阶段间通过 model transformation 与 justification links 串联，整体用于影响分析。 |
| P8 | **IVVQ 由能力/功能链/场景驱动** | 集成验证验证确认由模型中的 capability、functional chain、scenario 驱动，而非纯文本需求。 |
| P9 | **本质迭代、多生命周期** | 推荐 top-down，但支持 incremental / iterative / top-down / bottom-up / middle-out；不强制单一工程路径。 |
| P10 | **领域专用语言（DSL）** | 选用 DSL 而非 UML/SysML 等通用语言，降低非软件背景干系人的上手门槛。 |

---

## 3. 五个工程视角（Engineering Perspectives）

Arcadia 在给定工程层级（system / sub-system / software / hardware part…）
上按五个视角递进构建模型。每个视角产出一套"架构（architecture）"，并通过
justification links 与上一视角相连。

> 注：部分资料称"四层架构模型"，指前四个建模视角（OA/SA/LA/PA）；第五层
> EPBS 偏向契约与 IVVQ 准备，不在每个项目都建模。本规范按五视角完整收录。

### 3.1 运行分析 Operational Analysis（OA）——定义客户运行需求

- **别名**：Definition of the Problem / Customer Operational Need Analysis。
- **意图**：分析客户需求与目标、预期任务与活动，**远超系统需求本身**；在不
  定义系统的前提下理解"用户真正想做什么"。
- **目的**：确保系统定义相对于其真实运行使用与 IVVQ 条件是充分的；并为创新
  产品探索"感兴趣的系统实际上可能是什么"的备选方案。
- **主要步骤**：
  1. 定义运行参与者与实体（operational actors / entities）；
  2. 定义运行能力（operational capabilities）；
  3. 描述运行活动与能力场景（operational activities & capability scenarios）；
  4. 定义运行模式与状态（operational modes & states）；
  5. 将活动分配给运行参与者与实体。
- **输出**：一套"运行架构（operational architecture）"——以参与者/用户、
  运行能力与活动（含带维参的运行场景与运行约束如安全、保密、生命周期）描述
  并结构化需求。
- **典型图**：OAB（Operational Architecture Blank，运行架构图）、
  OCB（Operational Capabilities Blank，运行能力图）、
  OAIB（Operational Activity Interaction Blank，运行活动交互图）、
  MSM（Mode State Machine，模式与状态机图）。

### 3.2 系统分析 System Need Analysis（SA）——形式化系统需求

- **别名**：Formalization of system requirements / System Need Analysis。
- **意图**：聚焦**系统本身**，定义它如何满足前述运行需求及其预期行为与品质。
- **创建要素**：系统需支撑的功能（服务）及相关交换、非功能约束（安全、保密
  等）、分配到系统边界的性能、系统与操作员/外部系统的角色划分与交互、使用
  场景等。
- **目的**：**核对客户需求的可行性**（成本、进度、技术成熟度等），必要时提供
  重谈需求内容的依据；可附带一个初始系统架构设计模型以审视需求。
- **输出**：系统功能需求描述（功能、功能链、场景）、与用户/外部系统的互操作
  与交互（功能、交换 + 非功能约束）、系统需求。
- **关键性质**：OA 与 SA 这两视角构成架构构建的前半部分，**"规定"后续设计**，
  因此应经**客户批准/确认**。
- **典型图**：SAB（System Architecture Blank，系统架构图/系统数据流图）、
  系统接口、场景、MSM。

### 3.3 逻辑架构 Logical Architecture（LA）——概念解（Notional Solution）

- **别名**：Definition of solution architecture - Logical Architecture。
- **意图**：构建系统的**粗粒度组件分解**，承载最重要的工程决策，且在后续开发
  中不易被推翻；技术中立（technology neutral）。
- **过程**：从上一阶段功能/非功能需求出发，先定义解的预期行为（功能、接口、
  数据流、行为），再把系统分解为一个或多个**逻辑组件**，每个功能分配到一个
  组件。
- **决策准则**：纳入架构驱动因素与优先级、viewpoints 及其设计规则；对所有重大
  非功能约束（安全、保密、性能、IVV、成本、非技术…）进行比较求最佳折中
  （*viewpoint-driven*）。逻辑组件将倾向于成为开发/分包、集成、复用、产品与
  配置项定义的基础分解。
- **输出**：选定的逻辑架构——功能描述、组件与经论证的接口定义、场景、模式与
  状态，以及全部 viewpoints 及其在组件设计中如何被纳入的形式化；并与需求/运行
  场景建立链接。
- **典型图**：LAB（Logical Architecture Blank，逻辑架构图）、逻辑数据流图、
  逻辑组件/类、场景、MSM。

### 3.4 物理架构 Physical Architecture（PA）——最终解架构

- **别名**：Definition of solution architecture - Physical Architecture。
- **意图**：与逻辑架构构建相同意图，但定义本工程层级上系统的**"最终"架构**；
  完成后模型即视为**ready to develop**（交付给"更下"工程层级）。
- **新增内容**：进一步细节与设计决策、合理化、架构模式、新技术服务与行为组件，
  并按实现/技术/工艺约束与选择演进逻辑架构视图；**引入资源组件**（resource
  components）以承载先前的行为组件。沿用与逻辑层相同的 viewpoint-driven 方法。
- **输出**：选定的物理架构——待生产的组件、全部 viewpoints 及其在组件设计中
  的纳入方式；并与需求/运行场景建立链接。
- **协同工程落点**：物理架构是系统/软件/硬件干系人之间**协同工程
  （co-engineering）**的首选位置。
- **典型图**：PAB（Physical Architecture Blank，物理架构图）、物理数据流图、
  物理组件/类、接口、场景、MSM。

### 3.5 EPBS——组件契约与 IVVQ 准备

- **别名**：Building Strategy - Contracts for Development and IVVQ；EPBS =
  End-Product Breakdown Structure。
- **意图**：贡献一份 EPBS，并建模描述每个子系统/硬件/软件组件的规范；利用前序
  架构成果**形式化组件需求定义**并**为有保障的 IVVQ 做准备**。
- **核对内容**：此前所有与系统架构及组件相关的假设与施加约束在此汇总并校验。
- **输出**：主要是描述**组件集成契约（component integration contracts）**的
  新模型，汇集每个待开发组件所需的全部期望属性。
- **典型图**：EAB（EPBS Architecture Blank）。

### 阶段间关系一览

```
Operational Analysis ──need──▶ System Need Analysis ──need──▶ Logical Architecture
        │  justify                 │  justify                    │  justify
        ▼                          ▼                             ▼
   客户确认(批准)            客户确认(批准)              solution / 技术中立
                                                                     │
                                                                     ▼
                                              Physical Architecture ──▶ EPBS(契约/IVVQ)
                                                ready to develop
```

---

## 4. 核心概念词汇表

| 概念 | 定义 |
|------|------|
| **Capability（能力）** | 一个或多个实体为完成一个或多个任务所需的能力；细化需求，可由若干活动 + 一个场景描述。 |
| **Operational Actor / Entity** | 系统生命周期内将与之交互的运行参与者/实体（含用户、外部系统、环境）。 |
| **System Actor** | 系统边界外、与系统交互的参与者（操作员、外部系统）。 |
| **Function（功能）** | 系统执行的变换/动作；LA 前为"系统/逻辑功能"，PA 引入"技术功能/服务"。 |
| **Functional Chain（功能链）** | 跨功能的有序序列，描述端到端行为路径；也是 IVVQ 的驱动单元之一。 |
| **Scenario（场景）** | 参与者/实体/功能间交互的时序描述（能力场景、功能场景、组件场景等）。 |
| **Component（组件）** | 功能的承载单元；逻辑组件（LA）→ 物理组件（PA，含行为组件与资源组件）。 |
| **Interface（接口）** | 组件/角色之间交换与契约的定义。 |
| **Data / Exchange（数据/交换）** | 功能/组件间流动的信息。 |
| **Mode & State（模式与状态）** | 实体/组件/系统的运行模式与状态机；MSM 图描述。 |
| **Viewpoint（视角）** | 形式化某一非功能关切（安全、性能、实时、保密、可复用、成本、风险…）如何影响架构，用于求折中。 |
| **Justification Link** | 阶段间/元素间的论证链接，支撑影响分析与可追溯性。 |
| **Architecture Blank** | 每层的主架构图骨架（OAB/SAB/LAB/PAB/EAB），含参与者、功能、交换、组件。 |

---

## 5. Capella 图类型映射

Capella 为每个 Arcadia 视角提供一组图。命名约定为"层级前缀 + 图种类"。

| 层级 | 主架构图 | 能力/活动/场景 | 状态/模式 | 类/接口/需求 |
|------|----------|----------------|-----------|--------------|
| Operational | OAB | OCB（能力）、OAIB（活动交互）、OES（实体场景） | MSM | — |
| System | SAB | 系统能力图、系统功能交互、场景 | MSM | 系统接口、系统类 |
| Logical | LAB | 逻辑能力、逻辑功能交互、场景 | MSM | 逻辑类、逻辑接口 |
| Physical | PAB | 物理能力、物理功能交互、场景 | MSM | 物理类、物理接口 |
| EPBS | EAB | — | — | 组件契约 |

> **裁剪说明**：精确图缩写以 Capella 工具内置的方法论向导为准；本表给出的是
> 各层共有的图种类骨架，项目可按需取舍。Capella 自带方法论指导，模型组织以
> 一致方式自动完成，**无需像 SysML 那样手工用 Package 组织模型**。

---

## 6. 可追溯性（Traceability）

- 每个视角产出一个模型，模型间通过 **model transformation** 衍接，并通过
  **justification links** 关联；整体作为一个整体用于**影响分析**（如需求变更
  的影响评估）。
- 与需求的链接：需求可显示在任意图中，通过需求附件（requirement attachment）
  建立关系；可在 SMW 中创建需求或从 ReqIF 外部需求库导入。
- IVVQ 由模型中的 **capability / functional chain / scenario** 驱动，而非由
  文本需求驱动。

---

## 7. 视角驱动工程（Viewpoint-driven）

逻辑与物理架构的构建被描述为 *viewpoint-driven*：每个 viewpoint 形式化一类
非功能约束对架构的影响。常见 viewpoint 关切：功能一致性、接口、性能、实时、
安全、安全保密、集成、复用、成本、风险、进度、可适配性。组件分解的稳定性要求
所有重大非功能约束都被纳入并相互比较以找到**最佳折中**。

---

## 8. 生命周期与裁剪（Lifecycles & Adaptation）

- **推荐路径**：top-down——从运行/系统需求定义并验证需求，到技术中立的逻辑架构
  处理非功能约束，再到物理架构的技术功能/服务以最佳方式实现。
- **不强制**：Arcadia 可按多种生命周期与工作分担方案应用——
  *incremental / iterative / top-down / bottom-up / middle-out*。方法**本质
  迭代**。
- **非线性示例**：需求分析因运行知识不足而从需求起步（对运行需求做逆向工程）；
  需求分析提前到逻辑/物理架构以检验可行性；逻辑架构提前到部分物理架构以查
  性能；物理架构适配分包约束或由可复用既有组件装配；组件契约定义回溯物理架构
  以稳定集成。
- **领域裁剪**：每个组织应按自身业务、约束与 know-how **裁剪方法步骤**，包括：
  参考架构（含架构驱动因素）、适配域/产品/架构的 viewpoints、补充专用工程规则、
  相关架构模式选取、基于参考架构与 viewpoints 建模并支撑仿真/早期验证/设计流程
  自动化、各上下文调整规则、团队推广（培训/辅导）。

---

## 9. 协同工程与多级工程（Co-Engineering & Multi-Level）

- **协同工程**：物理架构是系统/软件/硬件干系人之间协同工程的首选位置；可通过
  协同模型、子系统需求模型的自动初始化、跨工程层级需求↔模型的影响分析支撑。
- **多级工程（递归）**：Arcadia 可在**每个系统分解层级上递归应用**——当前
  interest 的子系统成为下一层 interest 的系统，直至识别出单学科子系统、采购件
  或 COTS。第 n 层的物理架构定义上一层待开发组件（按对应组件集成契约）；第 n 层
  需求分析限定于该组件范围与邻域，以定义其 IVVQ 上下文并保护知识产权。

---

## 10. Arcadia vs SysML（对比要点）

| 维度 | Arcadia/Capella | SysML |
|------|-----------------|-------|
| 建模主线 | **功能驱动**（功能与接口为主线，需求与功能相连） | **需求驱动**（以需求为主线） |
| 起点倾向 | 从运行分析（OA）出发，探索"系统可能是什么"，利于创新 | 多从"黑盒系统"起步 |
| 语言性质 | 领域专用语言（DSL），面向非软件背景工程师 | 基于软件工程特性，跨行业工程师难掌握 |
| 模型一致性 | 元素集成度高，工具自带方法论指导，模型组织自动一致 | 元素间集成不足，易不一致；需手工 Package 组织 |
| 需求图 | 无专门需求图，需求可显示于任意图 | 提供专门需求图 |
| 状态/模式 | 提供模式与状态两类元素（MSM） | 仅用状态元素建模状态/模式 |
| 关系 | 受 SysML 启发，旨在**简化并丰富** SysML | 通用系统建模语言 |

> 适用得当，Arcadia 可有效开发系统架构模型，解决传统 SysML 应用面临的挑战；
> 但两者并非互斥——存在 Arcadia/Capella/SysML/工具间的等价映射。

---

## 11. Capella 工作台（Tooling）

- **Eclipse Capella™**：开源、可扩展的 MBSE 软件工具，实现 Arcadia 方法论，
  是覆盖工程各学科的**一致数字主线（digital thread）**基石。
- **能力**：方法论向导（embedded methodological guidance）、直观模型编辑、
  多视角查看、复杂度管理（掩蔽/限制/大规模建模/演进/复用机制）、可裁剪可集成。
- **生态**：开源与商业 Add-On（需求、协同、安全…），由全球 MBSE 专家网络支撑
  部署。
- **参考书**：
  - Jean-Luc Voirin《Model-based System and Architecture Engineering with the
    Arcadia Method》——方法基础与建模语言参考。
  - Pascal Roques《Systems Architecture Modeling with the Arcadia Method - A
    Practical Guide to Capella Modeling Tool》——工具实用指南。

---

## 12. 适用范围与限制

- **适用**：复杂系统/设备/软件/硬件架构定义；多约束折中；需早期验证与论证、
  跨干系人协同、可追溯 IVVQ 的项目；产品线变体与配置。
- **成本**：方法论与工具学习曲线、模型维护投入；小项目可能过重，应按 §8 裁剪。
- **非目标**：不规定存储/服务/查询基础设施；不替代领域专用 schema，而是引用之；
  不绑定单一工程路径或生命周期。

---

## 13. 一致性要求（Conformance）

一个工程产出（模型/文档集）**符合本 Arcadia-SPEC v0.1**，若：

1. **五视角可标识**：能指出 OA / SA / LA / PA / EPBS 各自的产出（EPBS 可裁剪
   缺省，但须显式声明裁剪理由）；
2. **need/solution 分层**：OA 与 SA 的产出经客户确认且仅描述 need；LA/PA/EPBS
   描述 solution；
3. **可追溯**：相邻视角之间存在 justification link 或等价追溯关系，支撑影响
   分析；
4. **功能驱动**：以功能与接口为主干组织模型，需求挂接到功能；
5. **viewpoint 显式**：LA/PA 的非功能约束以显式 viewpoint 表达并参与折中；
6. **生命周期声明**：声明所采用的生命周期（top-down / iterative / bottom-up /
   middle-out 之一或组合）与裁剪点。

消费方应将其他约束视为软指导，**不得**因以下情形拒绝一份产出：缺省 EPBS、
未使用的 viewpoint、自定义图布局、裁剪的子步骤——只要裁剪点与理由被显式记录。

---

# Citations

[1] Eclipse Foundation / PolarSys — *Capella MBSE Tool - Arcadia*.
    https://mbse-capella.org/arcadia.html
    （Arcadia 定义、五视角、原则、viewpoint、协同工程、多级工程、生命周期与裁剪）

[2] Eclipse Foundation — *Capella | Open Source MBSE Tool*.
    https://www.eclipse.org/capella/
    （Capella 工具定位、生态、参考书、案例）

[3] 火龙果软件 Alice 译 — *ARCADIA 和 SysML 方法在自适应巡航控制系统架构建模
    中的对比*.
    http://www.uml.org.cn/modeler/202110141.asp
    （Arcadia vs SysML、功能驱动 vs 需求驱动、OA 步骤与图类型 OCB/OAIB/OAB/MSM、
    模型组织方式对比）

[4] Jean-Luc Voirin — *Model-based System and Architecture Engineering with the
    Arcadia Method*. （方法基础与建模语言参考，引自 [1][2]）

[5] Pascal Roques — *Systems Architecture Modeling with the Arcadia Method -
    A Practical Guide to Capella Modeling Tool*. （Capella 实用指南，引自 [2]）
