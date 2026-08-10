# CPRIS 微信端 REST API 总览

静态扫描共识别 **179** 个对外 Controller 映射。

## 模块

| 模块 | 接口数 | 文档 |
|---|---:|---|
| `assess` | 37 | [assess](./modules/assess.md) |
| `children` | 20 | [children](./modules/children.md) |
| `parent` | 55 | [parent](./modules/parent.md) |
| `saas` | 20 | [saas](./modules/saas.md) |
| `training` | 42 | [training](./modules/training.md) |
| `user` | 5 | [user](./modules/user.md) |

## 说明

- 仅统计未被注释的 Spring MVC `@GetMapping`、`@PostMapping`、`@PutMapping`、`@DeleteMapping` 与 `@PatchMapping`。
- `DataController` 没有类级 `@RequestMapping`，其路由按方法注解直接记录。
- 每个接口详情提供源码位置、Java 方法签名、参数来源推断、返回声明和直接 Service/Mapper/Client 调用。
