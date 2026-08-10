# 运行时配置

## 默认网关

`https://teacherwx.cpris.com`

将此地址与接口路径拼接，例如：`https://teacherwx.cpris.com/user/info`。仅在用户明确提供其他网关时覆盖。

## 登录 Token

- 推荐凭据文件：`${CODEX_HOME}/cpris-wxapp-rest-api/credentials.json`；`CODEX_HOME` 未设置时使用 `~/.codex/cpris-wxapp-rest-api/credentials.json`。
- 保存最小字段：`gateway`、`authorization` 与 `validatedAt`。`authorization` 必须保存用户提供的完整请求头值（含其原有的 `Bearer ` 前缀）。
- 仅对 Base64/Base64URL 形式的长字符串进行候选检查；以 `GET /user/info` 返回的成功鉴权结果作为最终验证依据。收到 401、403、网络失败或无法确认的响应时，不保存或替换现有 Token。
- 凭据仅用于请求的 `Authorization` 头；不要在 URL、查询参数、版本库、Skill 文件、回复或日志中暴露。
