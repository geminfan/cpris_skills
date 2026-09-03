# GET /periodical/year/page

## 定位

- 模块：`training`
- Controller：`PeriodicalController`
- 源码：`cpris_wxapp/training/src/main/java/com/cpris/controller/PeriodicalController.java:381`
- Java 方法：`getPeriodicalPlanYearPage`

## 功能

分页查询。

## 请求

- HTTP 方法：`GET`
- 路径：`/periodical/year/page`
- 方法签名：`R<Page<TRecoverPeriodicalPlan>> getPeriodicalPlanYearPage(@ApiParam(value = "页码", example = "1") @RequestParam(defaultValue = "1") long current, @ApiParam(value = "查询日期（yyyy）不传默认今年", example = "2025") @RequestParam(required = false) String date, @ApiParam(value = "根据儿童姓名模糊查询条件", example = "宏观经济") @RequestParam(required = false) String childName)`

### 参数

- Query/表单：`@ApiParam(value = "页码", example = "1") @RequestParam(defaultValue = "1") long current`
- Query/表单：`@ApiParam(value = "查询日期（yyyy）不传默认今年", example = "2025") @RequestParam(required = false) String date`
- Query/表单：`@ApiParam(value = "根据儿童姓名模糊查询条件", example = "宏观经济") @RequestParam(required = false) String childName`

## 响应

- 声明返回类型：`R<Page<TRecoverPeriodicalPlan>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`periodicalPlanService.getPeriodicalTrainPageByYearAndUserIdAndChildName`

## 使用与安全提示

- AI 调用：经 AI 网关调用，受用户授权与运行时权限约束。
- 实际请求必须使用 AI 网关及 X-Api-Key；完整路径也不能绕过禁令，见 [网关契约](../gateway-contract.md)。
- 参数按完整 Java 参数分组并保留注解；DTO 字段与绑定规则见 [请求与响应约定](../schemas.md)。
- 源码路径相对于 cpris_wxapp 所在目录；行号与调用链为静态快照，收录不代表当前部署已开放。
