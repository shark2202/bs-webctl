Feature: 对已登录的真实标签页执行 JS 并取简化页面
  作为 AI agent
  我想要在不丢登录态的前提下扫描页面、执行脚本、拿到结果与 DOM 变化
  以便基于真实会话自动化浏览与操作

  # 对应 PRD-bs-webctl §3 路径 3

  Scenario: 无标签页连接时扫描报错
    Given 控制服务运行但无 Chrome 标签页连接
    When 用户请求扫描当前页
    Then 返回状态为错误并提示无标签页连接

  Scenario: 扫描返回当前页简化 HTML
    Given 一个已连接的标签页打开了某普通网页
    When 用户请求扫描当前页
    Then 返回状态为成功并含内容字段
    And 内容为简化后的 HTML

  Scenario: 仅文本扫描返回纯文本
    Given 一个已连接的标签页打开了某普通网页
    When 用户请求仅文本扫描
    Then 内容字段为纯文本且不含 HTML 标签

  Scenario: 执行 JavaScript 返回结果
    Given 一个已连接的标签页
    When 用户请求执行脚本获取页面标题
    Then 返回结果字段为该页面的标题

  Scenario: 执行结果可保存到文件
    Given 一个已连接的标签页
    When 用户请求执行脚本并保存结果到指定文件
    Then 该文件包含返回值
    And 返回结果字段提示已保存

  Scenario: 未提供脚本且未指定脚本文件时报错
    When 用户请求执行空脚本
    Then 返回状态为错误并提示未提供脚本
