# 运行时配置

## 默认网关

`https://teacherwx.cpris.com`

将此地址与接口路径拼接，例如：`https://teacherwx.cpris.com/user/info`。仅在用户明确提供其他网关时覆盖。

## 登录 Token

- 推荐凭据文件：`${CODEX_HOME}/cpris-wxapp-rest-api/credentials.json`；`CODEX_HOME` 未设置时使用 `~/.codex/cpris-wxapp-rest-api/credentials.json`。
- 保存最小字段：`gateway`、`authorization` 与 `validatedAt`。`authorization` 必须保存最终验证成功的完整请求头值（含验证成功时使用的 `Bearer ` 前缀，如有）。
- 每次 Skill 调用 API 时都先从该固定路径读取凭据，不能依赖对话记忆保存 Token。`gateway` 缺失时回退到本文件的默认网关。
- 仅对去掉可选 `Bearer ` 前缀后长度不少于 64、且符合 Base64/Base64URL 字符集的字符串进行候选检查。以 `GET /user/info` 返回的成功鉴权结果作为最终验证依据：先原样发送；仅在无前缀且收到 401/403 时重试一次 `Bearer <Token>`。收到网络失败或无法确认的响应时，不保存或替换现有 Token。
- 凭据仅用于请求的 `Authorization` 头；不要在 URL、查询参数、版本库、Skill 文件、回复或日志中暴露。
