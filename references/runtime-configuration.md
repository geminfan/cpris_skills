# 运行时配置

## 网关地址

本 Skill 只与 **AI 网关**通信，业务网关只是 AI 网关内部转发的目标，Skill 不直连。

| 角色 | 默认地址 | 谁在用 |
|---|---|---|
| **AI 网关**（`cpris_wxapp/ai` 模块，端口 3006） | `http://testai.cpris.com` | 本 Skill 的所有请求都发到这里 |
| **业务网关**（实际业务服务入口，含 saas/auth） | `http://test.cpris.com` | AI 网关内部转发用（服务端配置），Skill 不直接访问 |

AI 网关地址为**可配置的默认值**，覆盖优先级：

1. 环境变量 `CPRIS_AI_GATEWAY`
2. 凭据文件 `credentials.json` 里的 `gateway` 字段
3. 默认值 `http://testai.cpris.com`

无论取哪个值，请求都必须落在 AI 网关上：**禁止**把业务网关地址（`http://test.cpris.com`）或业务服务端口直接当作调用目标，那样会拿到未脱敏数据。

所有业务接口走 AI 网关前缀：

```
http://testai.cpris.com/ai/gw/{service}/{业务路径}
```

示例：`http://testai.cpris.com/ai/gw/user/user/info`。

健康检查 `GET /ai/gw/health` 在网关白名单内，无需认证，可用于探活。

## 服务端网关配置（了解即可，Skill 不改动）

AI 网关的 `application.yml`（前缀 `cpris.ai-gateway`）中与调用方相关的项：

```yaml
cpris:
  ai-gateway:
    enabled: true                       # false 时所有 /ai/gw/** 返回 503
    auth:
      auth-server-url: http://test.cpris.com   # 用 X-Api-Key 换登录 token 的 auth 服务地址
      token-path: /ai/key/token                # auth 侧换 token 的接口
      db-validate: true                        # 本地未配置的 key 交给 auth 查 t_ai_key 判定
      token-cache-seconds: 1800                # 网关内 token 缓存秒数
      api-keys:                                # 仅本地 ACL：路径/方法/限流
        - key: ak-cpris-ai-demo-0001
          allowed-paths: [/ai/gw/children/**, /ai/gw/user/**]   # 其余见 yml
          allowed-methods: GET,POST
          rate-limit-per-minute: 120
    routes:                             # 服务名 -> 业务网关基地址
      children: http://test.cpris.com
      user: http://test.cpris.com
      # merchant / parent / training / assess 同上
    masking:
      enabled: true                     # 响应递归脱敏总开关
```

`api-keys` 里配置的 key **只决定本地 ACL**，key 本身是否有效以 auth 服务的 `t_ai_key` 表为准；演示 key `ak-cpris-ai-demo-0001` 也必须在 `t_ai_key` 有对应记录，否则换不到 token（401）。

## AI 网关认证（X-Api-Key）

调用方的认证方式**仍然只是请求头 `X-Api-Key`**，换 token 的动作完全发生在 AI 网关内部：

```
Skill --X-Api-Key--> AI 网关 --X-Api-Key--> auth: POST /ai/key/token
                     AI 网关 <--accessToken(JWT)--
                     AI 网关 --Authorization: bearer {token}--> 业务服务
```

- 网关**不会**把 `X-Api-Key` 透传给下游业务服务；下游只看到 `Authorization: bearer {JWT}`。
- 调用方**不需要**、也不应该自己去请求 `/ai/key/token` 或自行携带 `Authorization` 头。
- auth 侧校验链：`t_ai_key` 中 `api_key` 命中且 `end_date` 为空或未过期 → 取绑定的 `merchant_id` / `employee_id` → `t_employee` 存在且 `is_login = 1` → 机构权限码非空 → 颁发与 `/login` 一致的 RS256 JWT。
- 换到的 token 在网关内按 key 缓存（默认 1800 秒），调用方无感知。

### 凭据管理

- **凭据文件路径**：`${HERMES_HOME}/cpris-wxapp-rest-api/credentials.json`；`HERMES_HOME` 未设置时使用 `~/.hermes/cpris-wxapp-rest-api/credentials.json`。
- **文件格式**：JSON 对象，包含 `gateway`（AI 网关地址，默认 `http://testai.cpris.com`）、`apiKey`（`t_ai_key` 中登记的 key 本体）与 `validatedAt`（ISO 8601 时间戳）。
- **自动注入**：每次 API 请求前从固定路径读取凭据，将 `apiKey` 字段值注入到 `X-Api-Key` 请求头。不依赖对话记忆保存 key。
- **验证规则**：
  - 仅对长度 ≥ 8、仅含 `A-Za-z0-9-_.` 字符的字符串进行候选检查（通常以 `ak-` 开头，不强制）
  - 验证顺序：先 `GET /ai/gw/health` 探活，再携带 `X-Api-Key` 请求 `GET /ai/gw/user/user/info`
  - `200` 视为验证成功并保存
  - `401` 视为 key 无效或已过期（`t_ai_key` 中查不到或 `end_date` 已过），不保存
  - `403` 需看响应 `msg` 区分：提示「无权访问此路径」= 本地 ACL 限制，key 有效，可保存并提示范围；其他（未绑定机构/用户、账号已禁用、机构已过期）= key 换不到 token，不保存
  - `405`/`429` 说明认证已通过、仅方法或频率受限，可保存
  - `502`（认证服务异常/下游异常）、`503`（网关停用或认证服务不可达）或网络失败：key 有效性无法确认，不保存或替换现有 key
- **Key 安全**：凭据仅用于 `X-Api-Key` 头；不在 URL、查询参数、版本库、Skill 文件、回复或日志中暴露。展示时仅保留首尾各 4 字符。

## 服务路由映射

| 业务路径前缀 | service |
|---|---|
| `/user` | `user` |
| `/childrenInfo`、`/guardian` | `children` |
| `/parent` | `parent` |
| `/training`、`/team`、`/periodical`、`/iepLib` | `training` |
| `/assess`、`/assessDefine`、`/assessGuide` | `assess` |

saas 模块（登录、短信验证码、数据字典等）未对 AI 网关开放，属敏感数据处理的正常规范，不得调用。auth 模块的 `/ai/key/token` 是网关内部用的换 token 接口，同样不对调用方开放。

## 敏感数据脱敏

AI 网关对 JSON 响应体递归脱敏后返回（姓名、身份证、手机号、邮箱、住址；含自由文本正则兜底）。脱敏后的数据必须原样使用，禁止还原、推断或绕过网关获取明文。详见 [SKILL.md](../SKILL.md) 的「敏感数据脱敏」章节。
