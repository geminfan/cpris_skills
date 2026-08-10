---
name: cpris-wxapp-rest-api
description: 查询和分析 CPRIS 微信端后端工程的 REST API。用于按业务或 URL 定位接口、解释请求参数和返回类型、追踪 Controller 到 Service/Mapper/Client 的直接调用、生成调用建议，或核对静态接口清单。
---

# CPRIS 微信端 REST API

使用此 Skill 说明 `C:\work\javacode\cpris_wxapp` 中的 Spring MVC 对外接口。

调用受保护接口前，提示用户自行配置有效的 Token；本 Skill 不保存、获取或自动注入 Token。

## 工作流程

1. 先读取 [API 总览](references/api-overview.md)，按 URL 或业务主题确认模块。
2. 读取对应的 `references/modules/<module>.md`，定位单接口详情。
3. 读取 `references/interfaces/` 下的接口文件，回答路径、HTTP 方法、参数、返回声明、源码位置和直接调用链。
4. 需要理解 JSON 字段时，依据详情中的 Java 返回/请求类型回到源工程检索 DTO、VO、Entity 与公共响应包装类型；不要把静态推断当成运行时契约。

## 文档边界

- 本 Skill 静态扫描了未注释的 Spring `@*Mapping` 方法；未包含网关前缀、Nacos/网关路由和运行时条件映射。
- 认证、租户和数据权限可能在网关、拦截器或 Service 层完成；接口详情未声明即表示 Controller 层未直接显示，而非无需认证。
- 每个接口文档中的调用链仅列出 Controller 方法体内能识别到的直接 `Service`、`Mapper` 或 `Client` 调用。

## 参考资料

- [模块与接口索引](references/api-overview.md)
- [请求与响应约定](references/schemas.md)
