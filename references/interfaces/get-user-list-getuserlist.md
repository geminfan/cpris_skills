# GET /user/list

## 定位

- 模块：`user`
- Controller：`UserController`
- 源码：`cpris_wxapp/user/src/main/java/com/cpris/controller/UserController.java:45`
- Java 方法：`getUserList`

## 功能

查询列表。

## 请求

- HTTP 方法：`GET`
- 路径：`/user/list`
- 方法签名：`R<List<TEmployee>> getUserList(@ApiParam(value = "用户名称", example = "小留学") String name, @ApiParam(value = "用户状态", example = "1") String status)`

### 参数

- Spring MVC 默认绑定：`@ApiParam(value = "用户名称", example = "小留学") String name`
- Spring MVC 默认绑定：`@ApiParam(value = "用户状态", example = "1") String status`

## 响应

- 声明返回类型：`R<List<TEmployee>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`employeeService.list`

## 使用与安全提示

- AI 调用：经 AI 网关调用，受用户授权与运行时权限约束。
- 实际请求必须使用 AI 网关及 X-Api-Key；完整路径也不能绕过禁令，见 [网关契约](../gateway-contract.md)。
- 参数按完整 Java 参数分组并保留注解；DTO 字段与绑定规则见 [请求与响应约定](../schemas.md)。
- 源码路径相对于 cpris_wxapp 所在目录；行号与调用链为静态快照，收录不代表当前部署已开放。
