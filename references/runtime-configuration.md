# 运行时配置

## 默认网关

**固定网关：`http://test.cpris.com`**

所有 API 请求必须使用此网关地址，不允许覆盖。将此地址与接口路径拼接，例如：`http://test.cpris.com/user/info`。

## 登录 Token

- **凭据文件路径**：`${HERMES_HOME}/cpris-wxapp-rest-api/credentials.json`；`HERMES_HOME` 未设置时使用 `~/.hermes/cpris-wxapp-rest-api/credentials.json`。
- **文件格式**：JSON 对象，包含 `gateway`（固定为 `http://test.cpris.com`）、`authorization`（完整请求头值，含 `Bearer ` 前缀）与 `validatedAt`（ISO 8601 时间戳）。
- **自动注入**：每次 API 请求前从固定路径读取凭据，将 `authorization` 字段值注入到 `Authorization` 请求头。不依赖对话记忆保存 Token。
- **验证规则**：
  - 仅对去掉可选 `Bearer ` 前缀后长度不少于 64、且符合 Base64/Base64URL 字符集的字符串进行候选检查
  - 使用 `GET /user/info` 验证：先原样发送；若无前缀且收到 401/403，重试一次 `Bearer <Token>`
  - 仅在 HTTP 200 且返回用户信息时视为验证成功，保存成功时使用的完整请求头值
  - 网络失败或无法确认的响应不保存或替换现有 Token
- **Token 安全**：凭据仅用于 `Authorization` 头；不在 URL、查询参数、版本库、Skill 文件、回复或日志中暴露。展示时仅保留首尾各 6 字符。
