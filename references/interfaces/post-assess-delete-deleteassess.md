# POST /assess/delete

## 定位

- 模块：`assess`
- Controller：`AssessController`
- 源码：`cpris_wxapp/assess/src/main/java/com/cpris/controller/AssessController.java:937`
- Java 方法：`deleteAssess`

## 功能

删除。

## 请求

- HTTP 方法：`POST`
- 路径：`/assess/delete`
- 方法签名：`R<String> deleteAssess(@RequestBody AssessVo assessVo)`

### 参数

- JSON 请求体：`@RequestBody AssessVo assessVo`

## 响应

- 声明返回类型：`R<String>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`assessResultValueService.remove`、`assessService.remove`

## 使用与安全提示

- AI 调用：禁止调用：网关删除禁令。
- 实际请求必须使用 AI 网关及 X-Api-Key；完整路径也不能绕过禁令，见 [网关契约](../gateway-contract.md)。
- 参数按完整 Java 参数分组并保留注解；DTO 字段与绑定规则见 [请求与响应约定](../schemas.md)。
- 源码路径相对于 cpris_wxapp 所在目录；行号与调用链为静态快照，收录不代表当前部署已开放。
