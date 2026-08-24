# 运行时配置

## 默认网关

**固定网关：`https://teacherwx.cpris.com`**

所有 API 请求必须使用此网关地址，不允许覆盖，不允许直连业务服务端口。所有业务接口走 AI 安全网关前缀：

```
https://teacherwx.cpris.com/ai/gw/{service}/{业务路径}
```

示例：`https://teacherwx.cpris.com/ai/gw/user/user/info`。

健康检查 `GET /ai/gw/health` 在网关白名单内，无需认证，可用于探活。

## AI 网关认证（X-Api-Key）

- **凭据文件路径**：`${HERMES_HOME}/cpris-wxapp-rest-api/credentials.json`；`HERMES_HOME` 未设置时使用 `~/.hermes/cpris-wxapp-rest-api/credentials.json`。
- **文件格式**：JSON 对象，包含 `gateway`（固定为 `https://teacherwx.cpris.com`）、`apiKey`（AI 网关签发的 key 本体）与 `validatedAt`（ISO 8601 时间戳）。
- **自动注入**：每次 API 请求前从固定路径读取凭据，将 `apiKey` 字段值注入到 `X-Api-Key` 请求头。不依赖对话记忆保存 key。
- **验证规则**：
  - 仅对长度 ≥ 8、仅含 `A-Za-z0-9-_.` 字符的字符串进行候选检查（通常以 `ak-` 开头，不强制）
  - 验证顺序：先 `GET /ai/gw/health` 探活，再携带 `X-Api-Key` 请求 `GET /ai/gw/user/user/info`
  - 返回 `401` 视为 key 无效；`200` 视为验证成功
  - `403`/`405`/`429`/`502` 说明认证已通过但权限/频率/下游受限：403+ 可保存 key 并提示权限范围；不因这些状态码否定 key 有效性
  - `503`（网关停用）或网络失败：key 有效性无法确认，不保存或替换现有 key
- **Key 安全**：凭据仅用于 `X-Api-Key` 头；不在 URL、查询参数、版本库、Skill 文件、回复或日志中暴露。展示时仅保留首尾各 4 字符。

## 服务路由映射

| 业务路径前缀 | service |
|---|---|
| `/user` | `user` |
| `/childrenInfo`、`/guardian` | `children` |
| `/parent` | `parent` |
| `/training`、`/team`、`/periodical`、`/iepLib` | `training` |
| `/assess`、`/assessDefine`、`/assessGuide` | `assess` |

saas 模块（登录、短信验证码、数据字典等）未对 AI 网关开放，属敏感数据处理的正常规范，不得调用。

## 敏感数据脱敏

AI 网关对 JSON 响应体递归脱敏后返回（姓名、身份证、手机号、邮箱、住址；含自由文本正则兜底）。脱敏后的数据必须原样使用，禁止还原、推断或绕过网关获取明文。详见 [SKILL.md](../SKILL.md) 的「敏感数据脱敏」章节。
