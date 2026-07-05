Feature: 启动服务后 Chrome 扩展自动连接
  作为 AI agent
  我想要启动本地服务后 Chrome 扩展自动连上
  以便不必手动配置连接，扩展加载即可用

  # 对应 PRD-bs-webctl §3 路径 2

  Scenario: 前台启动服务并监听本地端口
    Given bs-webctl 已安装
    When 用户请求启动控制服务
    Then WebSocket 服务监听本地回环地址的 18765 端口
    And HTTP 服务监听本地回环地址的 18766 端口
    And 标准错误流打印连接提示

  # 以下为集成场景，需真实 Chrome，归 step 4 闸门的集成层

  Scenario: 扩展加载后自动连接到已启动的服务
    Given 控制服务已在另一终端运行
    And Chrome 已加载 bs-webctl 扩展
    When 用户在 Chrome 打开任意普通网页
    Then 扩展自动连接到控制服务
    And 列出标签页命令能返回该标签页
