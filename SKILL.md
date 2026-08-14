---
name: cpris-wxapp-rest-api
description: 查询和分析 CPRIS 微信端后端工程的 REST API，自动管理认证 Token，调用受保护接口。用于按业务或 URL 定位接口、解释请求参数和返回类型、追踪 Controller 到 Service/Mapper/Client 的直接调用、生成调用建议、或核对静态接口清单。
---

# CPRIS 微信端 REST API

使用此 Skill 说明 `C:\work\javacode\cpris_wxapp` 中的 Spring MVC 对外接口。

**固定网关：`http://test.cpris.com`** — 所有 API 请求必须使用此网关，不允许覆盖。

## Token 自动管理

### 凭据存储位置

- **固定路径**：`${HERMES_HOME}/cpris-wxapp-rest-api/credentials.json`
- `HERMES_HOME` 未设置时使用 `~/.hermes/cpris-wxapp-rest-api/credentials.json`
- 目录和文件仅授予当前用户访问权限，绝不写入 Skill 目录、工作区或版本库

### 凭据文件格式

```json
{
  "gateway": "http://test.cpris.com",
  "authorization": "Bearer eyJhbGc...",
  "validatedAt": "2024-01-15T10:30:00Z"
}
```

### 自动认证流程

**每次调用此 Skill 时自动执行：**

1. **读取凭据**：尝试从固定路径读取 `credentials.json`
2. **检查状态**：
   - 若文件不存在或 `authorization` 字段为空 → 进入**请求认证**
   - 若存在有效凭据 → 使用现有 Token 继续执行
3. **请求认证**（当需要时）：
   - 友好提示用户："检测到未登录，请提供登录 Token 以继续操作。"
   - 说明 Token 格式：长度不少于 64 字符的 Base64/Base64URL 字符串，可选 `Bearer ` 前缀
   - 说明获取方式：可从微信开发者工具、浏览器 DevTools 或后端登录接口获取
4. **验证 Token**：
   - 用户提供 Token 后，使用 `http://test.cpris.com` 请求 `GET /user/info` 验证
   - 先以用户原样提供的值放入 `Authorization` 头
   - 若未带前缀且收到 `401`/`403` → 重试一次 `Bearer <Token>`
   - 仅在 HTTP 200 且返回用户信息时视为验证成功
5. **保存凭据**：
   - 验证成功后立即保存到固定路径
   - 保存时包含网关、完整 authorization 值（含前缀）和验证时间戳
6. **失败处理**：
   - Token 格式不符 → 提示格式要求，请求重新提供
   - 验证失败（401/403）→ 提示 Token 无效或已过期，请求重新提供
   - 网络失败 → 报告错误，不保存或覆盖现有 Token

### 辅助脚本（推荐）

`scripts/cpris_auth.py` 封装了完整的认证与调用流程，优先使用它而非手工拼 curl：

```bash
python scripts/cpris_auth.py login <token>     # 验证并持久化保存 Token
python scripts/cpris_auth.py status            # 查看登录状态（脱敏显示）
python scripts/cpris_auth.py logout            # 清除已保存的 Token
python scripts/cpris_auth.py call GET /user/info                    # 调用接口
python scripts/cpris_auth.py call POST /team/list --body '{"page":1}'
python scripts/cpris_auth.py call GET /training/list --query page=1 size=20
```

脚本自动完成：格式校验 → `GET /user/info` 验证 → 保存到固定凭据路径 → 后续调用自动注入 `Authorization` 头 → 遇 401/403 自动清除失效凭据。若环境无 Python，则按下方规则手工执行等价流程（curl + 读写 JSON 文件）。

### 使用规则

- **每次 API 调用前**：从固定路径读取 `authorization`，自动注入到 `Authorization` 请求头
- **不依赖对话记忆**：Token 仅从本地文件读取，不在对话上下文中保存
- **Token 安全**：
  - 不在回复、日志、命令输出或文档中回显完整 Token
  - 展示时仅保留首尾各 6 字符，如 `eyJhbG...Uw5fQ`
  - 不将 Token 写入 URL、查询参数或其他非请求头位置
- **清除 Token**：用户要求清除时，删除 `credentials.json` 文件

### Token 候选条件

仅当用户输入满足以下所有条件时，才视为 Token 候选：

1. 单独输入的字符串（不是 JSON 对象或其他结构化数据）
2. 去掉可选 `Bearer ` 前缀后长度 ≥ 64
3. 仅含 Base64/Base64URL 字符集：`A-Za-z0-9+/` 或 `A-Za-z0-9_-`，末尾可有 `=`

## 工作流程

**每次调用此 Skill 时，严格按以下顺序执行：**

1. **初始化认证**：
   - 读取 [运行时配置](references/runtime-configuration.md) 确认网关和凭据路径
   - 尝试从 `${HERMES_HOME}/cpris-wxapp-rest-api/credentials.json` 读取凭据
   - 若凭据不存在或无效 → 执行**自动认证流程**（见上方）
   - 认证成功后继续执行用户请求

2. **接口查询**（当需要调用 API 时）：
   - 读取 [API 总览](references/api-overview.md)，按 URL 或业务主题确认模块
   - 读取对应的 `references/modules/<module>.md`，定位单接口详情
   - 读取 `references/interfaces/` 下的接口文件，获取路径、HTTP 方法、参数、返回声明

3. **执行 API 请求**：
   - 使用固定网关 `http://test.cpris.com` 拼接接口路径
   - 从凭据文件读取 `authorization`，注入到 `Authorization` 请求头
   - 发送请求并处理响应
   - 若收到 `401`/`403` → Token 已失效，删除凭据文件，重新执行**自动认证流程**

4. **响应解析**（当需要理解返回字段时）：
   - 依据接口详情中的 Java 返回类型，到源工程检索 DTO、VO、Entity 类型
   - 不要把静态推断当成运行时契约，以实际返回 JSON 为准

## 文档边界

- 本 Skill 静态扫描了未注释的 Spring `@*Mapping` 方法；未包含网关前缀、Nacos/网关路由和运行时条件映射。
- 认证、租户和数据权限可能在网关、拦截器或 Service 层完成；接口详情未声明即表示 Controller 层未直接显示，而非无需认证。
- 每个接口文档中的调用链仅列出 Controller 方法体内能识别到的直接 `Service`、`Mapper` 或 `Client` 调用。

## 参考资料

- [模块与接口索引](references/api-overview.md)
- [请求与响应约定](references/schemas.md)
- [运行时配置](references/runtime-configuration.md)
