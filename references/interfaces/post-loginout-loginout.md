# POST /loginOut

## 定位

- 模块：`saas`
- Controller：`LoginController`
- 源码：`cpris_wxapp/saas/auth/src/main/java/com/cpris/controller/LoginController.java:113`
- Java 方法：`loginOut`

## 功能

登录。

## 请求

- HTTP 方法：`POST`
- 路径：`/loginOut`
- 方法签名：`R<String> loginOut(@ApiIgnore @RequestHeader(value = "Authorization", required = false) String authorizationHeader)`

### 参数

- 请求头：`@ApiIgnore @RequestHeader(value = "Authorization", required = false) String authorizationHeader`

## 响应

- 声明返回类型：`R<String>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

未检测到 Service / Mapper / Client 直接调用（可能为本地逻辑或调用名称未遵循约定）。

## 使用与安全提示

- AI 调用：不可调用：SaaS/登录/数据接口仅供源码参考。
- 实际请求必须使用 AI 网关及 X-Api-Key；完整路径也不能绕过禁令，见 [网关契约](../gateway-contract.md)。
- 参数按完整 Java 参数分组并保留注解；DTO 字段与绑定规则见 [请求与响应约定](../schemas.md)。
- 源码路径相对于 cpris_wxapp 所在目录；行号与调用链为静态快照，收录不代表当前部署已开放。
