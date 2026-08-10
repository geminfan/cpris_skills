# GET /training/dateRange/count

## 定位

- 模块：`training`
- Controller：`TrainingController`
- 源码：`C:\work\javacode\cpris_wxapp\training\src\main\java\com\cpris\controller\TrainingController.java:91`
- Java 方法：`getDateRangeCount`

## 功能

统计数量。

## 请求

- HTTP 方法：`GET`
- 路径：`/training/dateRange/count`
- 方法签名：`R<Map<String, Integer>> getDateRangeCount(@ApiParam(value = "开始日期（yyyy-MM-dd）", required = true, example = "2025-11-4") @RequestParam String startDate, @ApiParam(value = "结束日期（yyyy-MM-dd）", required = true, example = "2025-11-11") @RequestParam String endDate)`

### 参数

- 请求参数：`(value = "开始日期（yyyy-MM-dd）"`
- 请求参数：`required = true`
- Query 参数：`example = "2025-11-4") String startDate`
- 请求参数：`(value = "结束日期（yyyy-MM-dd）"`
- 请求参数：`required = true`
- Query 参数：`example = "2025-11-11") String endDate`

## 响应

- 声明返回类型：`R<Map<String, Integer>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`periodicalPlanService.getPeriodicalTrainCountByDateAndUserId`、`scheduleDefineService.getTeamTrainCountByDateAndUserId`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
