---
name: cpris-wxapp-rest-api
description: 查询和分析 CPRIS 微信端后端工程的 REST API，并按需验证和本地保存用户提供的登录 Token。用于按业务或 URL 定位接口、解释请求参数和返回类型、追踪 Controller 到 Service/Mapper/Client 的直接调用、生成调用建议、调用受保护接口，或核对静态接口清单。
---

# CPRIS 微信端 REST API

使用此 Skill 说明 `C:\work\javacode\cpris_wxapp` 中的 Spring MVC 对外接口。

默认网关为 `https://teacherwx.cpris.com`。除非用户明确指定其他网关，否则以该地址和接口路径拼接请求 URL。

## Token 管理

- 仅当用户单独输入或粘贴的字符串去掉可选 `Bearer ` 前缀后长度不少于 64，且仅含 Base64/Base64URL 字符（末尾可有 `=`）时，才将它作为候选登录 Token；不处理普通短文本、JSON 或密码。
- 先进行 Base64/Base64URL 格式检查（允许省略填充）；再使用默认网关请求 `GET /user/info` 验证。先以用户原样提供的值放入 `Authorization`；若未带前缀且收到 401/403，则仅额外重试一次 `Bearer <Token>`。仅在响应表明确认鉴权成功时，才将成功的请求头值作为登录 Token；格式可解码不代表已登录。
- 验证通过后，将原始 Token（及保留的认证前缀，如有）写入当前用户本机的 `${CODEX_HOME}/cpris-wxapp-rest-api/credentials.json`；若未设置 `CODEX_HOME`，推荐路径为 `~/.codex/cpris-wxapp-rest-api/credentials.json`。目录和文件仅授予当前用户访问权限，且绝不写入 Skill 目录、工作区或版本库。
- 每次调用此 Skill 处理 API 请求时，先记住并解析上述固定凭据路径；调用受保护接口前从该本地文件读取 `gateway` 与 `authorization`，并在 `Authorization` 请求头中自动注入保存的值。不要依赖对话记忆保存 Token。缺失、无效或过期时，提示用户重新提供 Token，不尝试获取或伪造 Token。
- 不在回复、日志、命令输出或文档中回显完整 Token；展示时仅保留首尾少量字符。用户要求清除 Token 时，删除上述本地凭据文件。

## 工作流程

1. 调用接口或管理 Token 时，先读取 [运行时配置](references/runtime-configuration.md)。
2. 先读取 [API 总览](references/api-overview.md)，按 URL 或业务主题确认模块。
3. 读取对应的 `references/modules/<module>.md`，定位单接口详情。
4. 读取 `references/interfaces/` 下的接口文件，回答路径、HTTP 方法、参数、返回声明、源码位置和直接调用链。
5. 需要理解 JSON 字段时，依据详情中的 Java 返回/请求类型回到源工程检索 DTO、VO、Entity 与公共响应包装类型；不要把静态推断当成运行时契约。

## 文档边界

- 本 Skill 静态扫描了未注释的 Spring `@*Mapping` 方法；未包含网关前缀、Nacos/网关路由和运行时条件映射。
- 认证、租户和数据权限可能在网关、拦截器或 Service 层完成；接口详情未声明即表示 Controller 层未直接显示，而非无需认证。
- 每个接口文档中的调用链仅列出 Controller 方法体内能识别到的直接 `Service`、`Mapper` 或 `Client` 调用。

## 参考资料

- [模块与接口索引](references/api-overview.md)
- [请求与响应约定](references/schemas.md)
- [运行时配置](references/runtime-configuration.md)
