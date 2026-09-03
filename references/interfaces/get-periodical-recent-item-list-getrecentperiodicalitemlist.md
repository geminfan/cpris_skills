# GET /periodical/recent/item/List

## 定位

- 模块：`training`
- Controller：`PeriodicalController`
- 源码：`cpris_wxapp/training/src/main/java/com/cpris/controller/PeriodicalController.java:146`
- Java 方法：`getRecentPeriodicalItemList`

## 功能

查询列表。

## 请求

- HTTP 方法：`GET`
- 路径：`/periodical/recent/item/List`
- 方法签名：`R<List<TRecoverPeriodicalPlan>> getRecentPeriodicalItemList(@ApiParam(value = "儿童id", required = true, example = "") @RequestParam String childId, @ApiParam(value = "康复指导文本模糊查询", example = "") @RequestParam String content)`

### 参数

- Query/表单：`@ApiParam(value = "儿童id", required = true, example = "") @RequestParam String childId`
- Query/表单：`@ApiParam(value = "康复指导文本模糊查询", example = "") @RequestParam String content`

## 响应

- 声明返回类型：`R<List<TRecoverPeriodicalPlan>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`periodicalPlanService.getRecentPeriodicalList`

## 使用与安全提示

- AI 调用：经 AI 网关调用，受用户授权与运行时权限约束。
- 实际请求必须使用 AI 网关及 X-Api-Key；完整路径也不能绕过禁令，见 [网关契约](../gateway-contract.md)。
- 参数按完整 Java 参数分组并保留注解；DTO 字段与绑定规则见 [请求与响应约定](../schemas.md)。
- 源码路径相对于 cpris_wxapp 所在目录；行号与调用链为静态快照，收录不代表当前部署已开放。
