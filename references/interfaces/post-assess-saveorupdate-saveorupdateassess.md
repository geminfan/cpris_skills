# POST /assess/saveOrUpdate

## 定位

- 模块：`assess`
- Controller：`AssessController`
- 源码：`cpris_wxapp/assess/src/main/java/com/cpris/controller/AssessController.java:137`
- Java 方法：`saveOrUpdateAssess`

## 功能

新增或更新。

## 请求

- HTTP 方法：`POST`
- 路径：`/assess/saveOrUpdate`
- 方法签名：`R<String> saveOrUpdateAssess(@RequestBody VSmdAssess assess)`

### 参数

- JSON 请求体：`@RequestBody VSmdAssess assess`
- 新建评估至少应包含 `childId`、`assessDefineId`、`assessProgress`、`assessDate`、`assessAppointDate`、`realAssessPerson`、`employeeId` 和 `assessType`。
- `assessDate` 和 `assessAppointDate` 使用 `yyyy-MM-dd HH:mm:ss`；评估老师账号同时写入 `realAssessPerson` 和 `employeeId`。`dgCreatedDate`、`dgCreatedBy` 是审计字段，不能替代上述业务字段。
- 能力评估（包括 C-PEP-3）使用 `assessType: "1"`。若原系统流程要求 `scheduleDefineId`，还必须先建立有效的排期关联，不能填入虚构 ID。

## 响应

- 声明返回类型：`R<String>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`smdAssessService.save`、`assessService.update`

## 使用与安全提示

- AI 调用：经 AI 网关调用，受用户授权与运行时权限约束。
- 实际请求必须使用 AI 网关及 X-Api-Key；完整路径也不能绕过禁令，见 [网关契约](../gateway-contract.md)。
- 参数按完整 Java 参数分组并保留注解；DTO 字段与绑定规则见 [请求与响应约定](../schemas.md)。
- 源码路径相对于 cpris_wxapp 所在目录；行号与调用链为静态快照，收录不代表当前部署已开放。
