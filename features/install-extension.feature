Feature: 一条命令装好 CLI 与 Chrome 扩展
  作为 AI agent 开发者
  我想要用一条命令释放并安装 Chrome 扩展
  以便快速进入浏览器控制能力，不必手动查找扩展文件

  # 对应 PRD-bs-webctl §3 路径 1

  Scenario: 首次安装扩展到用户目录
    Given bs-webctl 已安装且用户扩展目录不存在
    When 用户请求安装 Chrome 扩展
    Then 扩展被释放到用户扩展目录
    And 返回状态为成功并附扩展路径
    And 返回的加载指引指向 Chrome 扩展管理页

  Scenario: 扩展目录已存在且非空时拒绝覆盖
    Given 用户扩展目录已存在且非空
    When 用户请求安装 Chrome 扩展
    Then 返回状态为错误并提示目录已存在
    And 现有文件不被覆盖

  Scenario: 强制覆盖已存在的扩展
    Given 用户扩展目录已存在且非空
    When 用户请求强制安装 Chrome 扩展
    Then 扩展被重新释放覆盖原目录
    And 返回状态为成功
