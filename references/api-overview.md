# CPRIS 微信端 REST API 总览

静态扫描共识别 **179** 个对外 Controller 映射。

所有调用走 AI 安全网关：`http://testai.cpris.com/ai/gw/{service}/{业务路径}`（默认地址，可用 `CPRIS_AI_GATEWAY` 覆盖；`X-Api-Key` 认证，网关内部换取登录 token 后转发，响应已脱敏）。业务网关 `http://test.cpris.com` 由 AI 网关内部转发，不直连。服务映射与认证规范见 [运行时配置](runtime-configuration.md)。

## 模块

| 模块 | 接口数 | 网关 service | 文档 |
|---|---:|---|---|
| `assess` | 37 | `assess` | [assess](./modules/assess.md) |
| `children` | 20 | `children` | [children](./modules/children.md) |
| `parent` | 55 | `parent` | [parent](./modules/parent.md) |
| `saas` | 20 | —（未对 AI 网关开放） | [saas](./modules/saas.md) |
| `training` | 42 | `training` | [training](./modules/training.md) |
| `user` | 5 | `user` | [user](./modules/user.md) |

## 说明

- 仅统计未被注释的 Spring MVC `@GetMapping`、`@PostMapping`、`@PutMapping`、`@DeleteMapping` 与 `@PatchMapping`。
- `DataController` 没有类级 `@RequestMapping`，其路由按方法注解直接记录。
- 每个接口详情提供源码位置、Java 方法签名、参数来源推断、返回声明和直接 Service/Mapper/Client 调用。
