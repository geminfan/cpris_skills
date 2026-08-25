---
name: cpris-wxapp-rest-api
description: 查询和分析 CPRIS 微信端后端工程的 REST API，通过 AI 安全网关调用受保护接口，自动管理 API-Key 凭据，响应数据已经过敏感信息脱敏。用于按业务或 URL 定位接口、解释请求参数和返回类型、追踪 Controller 到 Service/Mapper/Client 的直接调用、生成调用建议、或核对静态接口清单。
---

# CPRIS 微信端 REST API（AI 安全网关版）

## 关于希普在线

**希普在线（CPRIS）** 是一个专业的 **孤独症（自闭症）康复机构一体化管理平台**，致力于为特殊儿童康复提供智慧化解决方案。

**官方网站**：[www.cpris.com](https://www.cpris.com)

### 平台定位

希普在线是国内领先的孤独症儿童康复服务平台，已在全国 28 个省 700 多个孤独症康复机构使用，累计儿童服务量超过 200 万人次。

### 核心能力

- **专业评估体系**：植入 C-PEP-3（孤独症谱系及相关发育障碍心理教育评定量表）中国常模数据，提供标准化评估服务
- **智慧康复管理**：为康复机构提供从评估、IEP 计划、教学实施到效果追踪的全流程数字化管理
- **多角色服务**：覆盖民营机构、医疗科室、主管单位和家长四大服务场景
- **专家团队支持**：由北京大学第六医院、辽宁师范大学等顶级专家团队提供技术指导

### 技术架构

本 Skill 对接的是希普在线微信小程序后端 REST API。所有调用必须经过 **AI 安全网关**（`cpris_wxapp/ai` 模块，Spring Boot，端口 3006）：网关统一执行 API-Key 认证、用 API-Key 到 auth 服务换取登录 token 再转发、路径/方法权限校验、限流，并在返回前对响应体做**递归敏感数据脱敏**。

---

## 网关地址

| 角色 | 默认地址 | 说明 |
|---|---|---|
| **AI 网关** | `http://testai.cpris.com` | 本 Skill 唯一的请求目标 |
| **业务网关** | `http://test.cpris.com` | 实际业务服务入口，由 AI 网关内部转发，**Skill 不直连** |

AI 网关地址是**可配置的默认值**，覆盖优先级：环境变量 `CPRIS_AI_GATEWAY` > 凭据文件 `gateway` 字段 > 默认 `http://testai.cpris.com`。

不论配置成什么，请求都必须落在 AI 网关上：不允许直接访问业务网关 `http://test.cpris.com` 或业务服务端口，那样绕过了脱敏与鉴权。

## AI 网关调用规范（必须遵守）

### 路径规则

所有业务接口通过网关转发，路径格式：

```
http://testai.cpris.com/ai/gw/{service}/{业务路径...}
```

示例：`GET /ai/gw/children/childrenInfo/page?current=1` → 网关转发到 children 服务 `GET /childrenInfo/page?current=1`。

### 服务路由映射

根据业务路径第一段确定 `{service}`：

| 业务路径前缀 | service | 模块文档 |
|---|---|---|
| `/user` | `user` | [user](references/modules/user.md) |
| `/childrenInfo`、`/guardian` | `children` | [children](references/modules/children.md) |
| `/parent` | `parent` | [parent](references/modules/parent.md) |
| `/training`、`/team`、`/periodical`、`/iepLib` | `training` | [training](references/modules/training.md) |
| `/assess`、`/assessDefine`、`/assessGuide` | `assess` | [assess](references/modules/assess.md) |

**注意**：saas 模块的登录/验证码类接口（`/login`、`/loginOut`、`/phone/**`、`/wx/**`、`/parent/phone/login`、`/parent/wx/login`）及数据字典接口（`/data/map`、`/nation/list` 等）**未对 AI 网关开放**——这是敏感数据处理的正常规范，登录凭证和短信通道不对 AI 技能暴露。不要尝试调用它们。

### 认证

**对调用方而言，认证方式只有一个：请求头 `X-Api-Key: <api key>`**（不要自己带 `Authorization` 头）。

网关内部的处理链路（调用方无需参与）：

```
Skill --X-Api-Key--> AI 网关 --X-Api-Key--> auth: POST /ai/key/token
                     AI 网关 <--accessToken(JWT)--
                     AI 网关 --Authorization: bearer {token}--> 业务服务
```

- AI 网关拿请求头里的 `X-Api-Key` 到 auth 服务换一个登录 JWT，用 `Authorization: bearer {token}` 转发给下游；**`X-Api-Key` 不透传给业务服务**
- 换到的 token 在网关内按 key 缓存（默认 1800 秒），对调用方透明
- key 是否有效由 auth 查 `t_ai_key` 表判定：`api_key` 命中且 `end_date` 为空或未过期 → 取绑定的 `merchant_id`/`employee_id` → `t_employee` 存在且 `is_login = 1` → 机构权限码非空 → 颁发 JWT。**数据权限即该 key 绑定用户本人的权限**
- 网关 yml 的 `cpris.ai-gateway.auth.api-keys` 只是**本地 ACL**（允许路径 Ant 通配、允许方法、限流阈值），不决定 key 是否有效；yml 里没配的 key 在 `db-validate: true`（默认）时直接放行到换 token 环节，由 `t_ai_key` 判定，本地不再做路径/方法/限流限制
- 演示 key `ak-cpris-ai-demo-0001` 同样必须在 `t_ai_key` 表中有记录，否则换不到 token（401）
- auth 的 `POST /ai/key/token` 是网关内部接口，Skill 不得直接调用

### 错误码语义

| HTTP 状态 | 含义 | 处理 |
|---|---|---|
| 401 | 缺少 `X-Api-Key`；或 key 在 `t_ai_key` 中不存在 / `end_date` 已过期 | 清除本地凭据，请求用户提供新 key |
| 403 | 两种情况，看响应 `msg`：① 本地 ACL 拒绝（「无权访问此路径」）；② key 有效但无登录资格（未绑定机构/用户、机构不存在、绑定用户不存在、账号已禁用 `is_login≠1`、机构已过期） | ① 保留凭据，不要重试该路径；② 保留凭据并提示管理员修正 `t_ai_key`/`t_employee` 绑定，该 key 当前换不到 token |
| 405 | 该 key 不允许使用此 HTTP 方法（仅本地配了 ACL 的 key 会出现） | 换用允许的方法（GET/POST） |
| 429 | 触发限流（每分钟上限，仅本地配了 ACL 的 key 会出现） | 等待约 60 秒再重试 |
| 502 | 认证服务返回异常或未返回 token；下游服务不可达；响应脱敏处理失败 | 报告错误；不要尝试绕过网关重试 |
| 503 | AI 网关总开关已关闭，或认证服务（auth）不可达 | 报告错误等待管理员处理；此时无法确认 key 有效性，不要清除凭据 |

`GET /ai/gw/health` 在白名单内，无需 key，可用于探测网关可达性。

### 敏感数据脱敏（合规红线）

网关对 JSON 响应体做递归脱敏后再返回，两道防线：字段名规则（name/idcard/phone/email/address 等）+ 内容正则兜底（自由文本中夹带的手机号/身份证/邮箱）。

脱敏样式：

```
姓名    王小明              -> 王**
身份证  360123200001011234  -> 360****1234
手机号  13812345678         -> 138****5678
邮箱    zhangsan@example.com -> z****n@example.com
住址    广东省广州市天河区xx路123号 -> 广东省广州市****
```

**合规要求：**

1. **直接使用脱敏后的数据**，禁止尝试还原、猜测、补全或推断被脱敏的字段
2. 禁止用脱敏后数据与其他数据交叉比对做重识别
3. 禁止绕过网关（直连业务服务、伪造路径、拼接非 `/ai/gw/` 前缀）获取未脱敏数据
4. 展示响应中的敏感字段时，保持网关返回的脱敏形态原样呈现
5. 系统字段（childid、merchantid、code、msg、分页字段等）不脱敏，可正常使用

## API-Key 自动管理

### 凭据存储位置

- **固定路径**：`${HERMES_HOME}/cpris-wxapp-rest-api/credentials.json`
- `HERMES_HOME` 未设置时使用 `~/.hermes/cpris-wxapp-rest-api/credentials.json`
- 目录和文件仅授予当前用户访问权限，绝不写入 Skill 目录、工作区或版本库

### 凭据文件格式

```json
{
  "gateway": "http://testai.cpris.com",
  "apiKey": "ak-xxxxxxxx-xxxx",
  "validatedAt": "2026-08-21T10:30:00Z"
}
```

（凭据文件不再保存 `authorization` Bearer Token：调用方只需提供 `X-Api-Key`，下游业务服务所需的登录 token 由 AI 网关内部用该 key 换取。）

### 自动认证流程

**每次调用此 Skill 时自动执行：**

1. **读取凭据**：尝试从固定路径读取 `credentials.json`
2. **检查状态**：
   - 若文件不存在或 `apiKey` 字段为空 → 进入**请求认证**
   - 若存在有效凭据 → 使用现有 key 继续执行
3. **请求认证**（当需要时）：
   - 友好提示用户："检测到未配置 AI 网关 API-Key，请提供以继续操作。"
   - 说明格式：AI 网关签发的 key（示例形如 `ak-cpris-ai-xxxx`），长度不少于 8 字符，不含空白
   - 说明获取方式：向平台管理员申请，由管理员在 auth 的 `t_ai_key` 表登记（绑定 `merchant_id`/`employee_id`，可选 `end_date`）；如需额外的路径/方法/限流限制，再到网关 yml 的 `cpris.ai-gateway.auth.api-keys` 补 ACL
4. **验证 API-Key**：
   - 先请求 `GET /ai/gw/health`（白名单）确认网关可达
   - 再携带 `X-Api-Key` 请求 `GET /ai/gw/user/user/info` 验证
   - `200` → 验证成功，保存
   - `401`（key 不存在或已过期）→ 验证失败，不保存
   - `403` → 看响应 `msg`：含「无权访问此路径」说明只是本地 ACL 受限、key 有效，可保存并提示范围；其他 403（绑定/账号/机构问题）说明该 key 换不到 token，不保存
   - `405`/`429` → 认证已通过、仅方法或频率受限，可保存
   - `502`/`503`（认证服务异常或不可达、网关停用）→ key 有效性无法确认，不保存也不覆盖现有 key
5. **保存凭据**：
   - 验证成功后立即保存到固定路径，包含网关、key 本体和验证时间戳
6. **失败处理**：
   - key 格式不符 → 提示格式要求，请求重新提供
   - 验证失败（401）→ 提示 key 无效，请求重新提供
   - 网络失败、网关停用或认证服务不可达（502/503）→ 报告错误，不保存或覆盖现有 key

### 辅助脚本（推荐）

`scripts/cpris_auth.py` 封装了完整的认证与调用流程，优先使用它而非手工拼 curl：

```bash
python scripts/cpris_auth.py login <api-key>   # 验证并持久化保存 API-Key
python scripts/cpris_auth.py status            # 查看配置状态（脱敏显示）
python scripts/cpris_auth.py logout            # 清除已保存的 API-Key
python scripts/cpris_auth.py call GET /user/info                    # 调用接口（自动补 /ai/gw/user 前缀）
python scripts/cpris_auth.py call POST /team/list --body '{"page":1}'
python scripts/cpris_auth.py call GET /training/list --query page=1 size=20
python scripts/cpris_auth.py call GET /ai/gw/children/childrenInfo/page --query current=1   # 完整网关路径亦可
```

脚本自动完成：格式校验 → `GET /ai/gw/health` 探活 → `GET /ai/gw/user/user/info` 验证 key → 保存到固定凭据路径 → 后续调用自动注入 `X-Api-Key` 头、按业务路径自动补 `/ai/gw/{service}` 前缀 → 遇 401 自动清除失效凭据，403/405/429/502/503 按网关错误语义提示。网关地址取环境变量 `CPRIS_AI_GATEWAY`，未设置时用默认 `http://testai.cpris.com`。若环境无 Python，则按上方规则手工执行等价流程（curl + 读写 JSON 文件）。

### 使用规则

- **每次 API 调用前**：从固定路径读取 `apiKey`，自动注入到 `X-Api-Key` 请求头
- **不依赖对话记忆**：key 仅从本地文件读取，不在对话上下文中保存
- **Key 安全**：
  - 不在回复、日志、命令输出或文档中回显完整 key
  - 展示时仅保留首尾各 4 字符，如 `ak-c****0001`
  - 不将 key 写入 URL、查询参数或其他非请求头位置
- **清除 key**：用户要求清除时，删除 `credentials.json` 文件

### API-Key 候选条件

仅当用户输入满足以下所有条件时，才视为 API-Key 候选：

1. 单独输入的字符串（不是 JSON 对象或其他结构化数据）
2. 长度 ≥ 8
3. 仅含 `A-Za-z0-9-_.` 字符，无空白（通常以 `ak-` 开头，但不强制）

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
   - 按服务路由映射把业务路径换算为 AI 网关路径：`http://testai.cpris.com/ai/gw/{service}/{业务路径}`
   - 从凭据文件读取 `apiKey`，注入到 `X-Api-Key` 请求头（不要自己拼 `Authorization` 头，换 token 由网关内部完成）
   - 发送请求并处理响应；错误码按上方**错误码语义**处理
   - saas 登录类接口不在开放范围，直接说明并拒绝调用

4. **响应解析**（当需要理解返回字段时）：
   - 响应已经过网关脱敏，敏感字段保持脱敏形态直接使用
   - 依据接口详情中的 Java 返回类型，到源工程检索 DTO、VO、Entity 类型
   - 不要把静态推断当成运行时契约，以实际返回 JSON 为准

## 文档边界

- 本 Skill 静态扫描了未注释的 Spring `@*Mapping` 方法；未包含网关前缀、Nacos/网关路由和运行时条件映射。
- 认证、租户和数据权限由 AI 网关过滤器与网关换取的登录 token 共同决定（token 绑定 `t_ai_key` 指定的机构与员工）；接口详情未声明即表示 Controller 层未直接显示，而非无需认证。
- 每个接口文档中的调用链仅列出 Controller 方法体内能识别到的直接 `Service`、`Mapper` 或 `Client` 调用。
- 接口文档中的字段名基于源码静态生成；实际响应中敏感字段值已被网关脱敏，与源码字段定义的字面值不同属于正常现象。

## 参考资料

- [模块与接口索引](references/api-overview.md)
- [请求与响应约定](references/schemas.md)
- [运行时配置](references/runtime-configuration.md)
