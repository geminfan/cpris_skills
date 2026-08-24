# CPRIS Skills

面向 CPRIS 项目的 Codex Skills 集合。

## 已收录

### `cpris-wxapp-rest-api`

基于 `cpris_wxapp` Spring MVC 源码静态扫描生成的 REST API 查询与分析 Skill，调用链路经过 `cpris_wxapp/ai` 模块的 **AI 安全网关**。

- 固定网关：`https://teacherwx.cpris.com`，业务接口走 `/ai/gw/{service}/**` 前缀
- 认证方式：请求头 `X-Api-Key`（AI 网关签发，绑定允许路径/方法与限流阈值）。用户粘贴 key 后，Skill 先 `GET /ai/gw/health` 探活，再以 `GET /ai/gw/user/user/info` 验证；验证成功后保存到 `${CODEX_HOME}/cpris-wxapp-rest-api/credentials.json`（未设置时为 `~/.codex/cpris-wxapp-rest-api/credentials.json`）。每次后续调用都会从该路径读取并注入 `X-Api-Key` 头
- 敏感数据合规：网关对 JSON 响应递归脱敏（姓名/身份证/手机号/邮箱/住址），Skill 直接使用脱敏后数据，禁止还原或绕过网关
- saas 模块登录/短信/数据字典接口未对 AI 网关开放（敏感数据处理规范），Skill 拒绝调用

- 覆盖 179 个已识别的对外接口
- 覆盖评估、儿童、家长、SaaS、训练和用户 6 个模块
- 按“总览 → 模块 → 单接口”组织文档，适合按 URL 或业务快速定位
- 单接口文档包含 HTTP 方法、路径、Controller 源码位置、Java 方法签名、参数来源、返回声明及直接调用链

目录：

```text
cpris-wxapp-rest-api/
├── SKILL.md
├── agents/openai.yaml
├── scripts/cpris_auth.py
└── references/
    ├── api-overview.md
    ├── runtime-configuration.md
    ├── schemas.md
    ├── modules/
    └── interfaces/
```

## 使用

在支持 Codex Skills 的环境中安装或引用 `cpris-wxapp-rest-api` 目录，然后使用类似下面的提示：

```text
Use $cpris-wxapp-rest-api to find and explain the endpoint for parent assessment results.
```

也可以直接阅读 `cpris-wxapp-rest-api/references/api-overview.md`，从模块索引进入单接口文档。

## 生成边界

该 Skill 基于源码中的 Spring MVC 映射注解静态生成。网关前缀、运行时路由条件、认证与数据权限策略，以及 DTO/VO 的完整 JSON 字段，需要结合实际部署配置和源码进一步确认。实际响应中敏感字段值已被 AI 网关脱敏，与源码定义的字面值不同属于正常现象。
