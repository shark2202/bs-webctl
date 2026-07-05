---
type: PRD
prd: PRD-bs-webctl
title: bs-webctl 独立浏览器控制 CLI
description: 给 AI agent 提供"控制真实 Chrome、保留登录态"的标准原语，三问封顶。
status: accepted
date: 2026-07-05
tags: [cli, browser, ai-agent, websocket]
timestamp: 2026-07-05T00:00:00Z
---
# PRD: bs-webctl 独立浏览器控制 CLI

## 1. 为什么存在

给 AI agent 一个"控制真实 Chrome、保留登录态"的标准原语包，`pip install`
即用，避免每个 agent 重造浏览器自动化的轮子。

## 2. 解决什么问题

- **Selenium/Playwright**：起独立浏览器实例，丢登录态、占资源、难复用人工
  会话 —— agent 想用的是"我正在用的这个 Chrome"，不是一个新实例。
- **裸 CDP**：太低层，agent 要的是"扫描页面拿简化 HTML""执行 JS 拿结果+DOM
  diff"这种原语，不是手撸 WebSocket 帧。
- **复制粘贴**：每个 agent 各写一套浏览器胶水，drift 严重、bug 各修各的。

没有 bs-webctl 时：agent 要么绑在重框架上丢登录态，要么自己写胶水。

## 3. 用户怎么走

1. `pip install bs-webctl` + `bs-webctl install-extension` —— 装 CLI、释放
   Chrome MV3 扩展到 `~/.bs-webctl/extension/`。
2. `bs-webctl server` 起常驻服务；Chrome 加载扩展，扩展自动连上 WS
   `127.0.0.1:18765`。
3. `bs-webctl sessions` / `scan` / `exec` / `exec-file` 操纵已登录的真实
   标签页，输出 JSON 到 stdout 供 agent 程序化解析。

每条路径对应一个 BDD feature：[`install-extension`](../features/install-extension.feature) / [`server-connect`](../features/server-connect.feature) / [`scan-exec`](../features/scan-exec.feature)。step 定义与 runner 选型随闸门落地（待 ADR-0003）。
