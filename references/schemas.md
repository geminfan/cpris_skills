# 请求与响应约定

## 请求参数

- 标有 `@RequestBody` 的参数为 JSON 请求体。
- 标有 `@RequestParam`、`@PathVariable`、`@RequestHeader` 的参数分别来自 Query、路径和请求头。
- 未标注参数的绑定行为受 Spring MVC 配置影响，应以方法签名与前端调用为准。

## 响应

- 接口详情中的“声明返回类型”来自 Controller 方法签名。
- 具体响应 JSON 字段由 `Result` / DTO / VO / Entity 等类型定义决定；可根据详情页的返回类型继续在源码中检索。
