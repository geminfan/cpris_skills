# GET /sysBasedata/list

## 定位

- 模块：`saas`
- Controller：`DataController`
- 源码：`cpris_wxapp/saas/auth/src/main/java/com/cpris/controller/DataController.java:105`
- Java 方法：`getKinshipList`

## 功能

查询列表。

## 请求

- HTTP 方法：`GET`
- 路径：`/sysBasedata/list`
- 方法签名：`R<Map<String, List<SysBasedata>>> getKinshipList(@ApiParam(value = "数据字典类型代码列表", required = true) @RequestParam List<String> dataTypes)`

### 参数

- Query/表单：`@ApiParam(value = "数据字典类型代码列表", required = true) @RequestParam List<String> dataTypes`

## 响应

- 声明返回类型：`R<Map<String, List<SysBasedata>>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`sysBasedataService.list`

## 使用与安全提示

- AI 调用：不可调用：SaaS/登录/数据接口仅供源码参考。
- 实际请求必须使用 AI 网关及 X-Api-Key；完整路径也不能绕过禁令，见 [网关契约](../gateway-contract.md)。
- 参数按完整 Java 参数分组并保留注解；DTO 字段与绑定规则见 [请求与响应约定](../schemas.md)。
- 源码路径相对于 cpris_wxapp 所在目录；行号与调用链为静态快照，收录不代表当前部署已开放。
