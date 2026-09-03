# GET /training/dateRange/count

## 定位

- 模块：`training`
- Controller：`TrainingController`
- 源码：`cpris_wxapp/training/src/main/java/com/cpris/controller/TrainingController.java:91`
- Java 方法：`getDateRangeCount`

## 功能

统计数量。

## 请求

- HTTP 方法：`GET`
- 路径：`/training/dateRange/count`
- 方法签名：`R<Map<String, Integer>> getDateRangeCount(@ApiParam(value = "开始日期（yyyy-MM-dd）", required = true, example = "2025-11-4") @RequestParam String startDate, @ApiParam(value = "结束日期（yyyy-MM-dd）", required = true, example = "2025-11-11") @RequestParam String endDate)`

### 参数

- Query/表单：`@ApiParam(value = "开始日期（yyyy-MM-dd）", required = true, example = "2025-11-4") @RequestParam String startDate`
- Query/表单：`@ApiParam(value = "结束日期（yyyy-MM-dd）", required = true, example = "2025-11-11") @RequestParam String endDate`

## 响应

- 声明返回类型：`R<Map<String, Integer>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`periodicalPlanService.getPeriodicalTrainCountByDateAndUserId`、`scheduleDefineService.getTeamTrainCountByDateAndUserId`

## 使用与安全提示

- AI 调用：经 AI 网关调用，受用户授权与运行时权限约束。
- 实际请求必须使用 AI 网关及 X-Api-Key；完整路径也不能绕过禁令，见 [网关契约](../gateway-contract.md)。
- 参数按完整 Java 参数分组并保留注解；DTO 字段与绑定规则见 [请求与响应约定](../schemas.md)。
- 源码路径相对于 cpris_wxapp 所在目录；行号与调用链为静态快照，收录不代表当前部署已开放。
