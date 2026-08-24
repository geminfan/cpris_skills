# 请求与响应约定

## 网关路径换算

接口文档中的路径均为业务路径，调用时需换算为 AI 网关路径：

```
https://teacherwx.cpris.com/ai/gw/{service}/{业务路径}
```

示例：文档路径 `/childrenInfo/page` → 网关路径 `/ai/gw/children/childrenInfo/page`。服务映射见 [运行时配置](runtime-configuration.md)。

## 请求参数

- 标有 `@RequestBody` 的参数为 JSON 请求体。
- 标有 `@RequestParam`、`@PathVariable`、`@RequestHeader` 的参数分别来自 Query、路径和请求头。
- 未标注参数的绑定行为受 Spring MVC 配置影响，应以方法签名与前端调用为准。

## 响应

- 接口详情中的“声明返回类型”来自 Controller 方法签名。
- 具体响应 JSON 字段由 `Result` / DTO / VO / Entity 等类型定义决定；可根据详情页的返回类型继续在源码中检索。
- **实际响应已经过 AI 网关敏感数据脱敏**（姓名、身份证、手机号、邮箱、住址；自由文本中的同类内容也会被正则兜底脱敏）。脱敏后的值（如 `138****5678`）即为最终交付形态，禁止还原或推断。系统字段（childid、merchantid、code、msg、分页字段等）不脱敏。
- 网关错误响应统一为 `{"code":<http 状态>, "msg":"<说明>"}`，状态码语义见 [SKILL.md](../SKILL.md) 的「错误码语义」。
