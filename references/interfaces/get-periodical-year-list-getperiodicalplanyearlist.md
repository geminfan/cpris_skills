# GET /periodical/year/list

## 定位

- 模块：`training`
- Controller：`PeriodicalController`
- 源码：`C:\work\javacode\cpris_wxapp\training\src\main\java\com\cpris\controller\PeriodicalController.java:362`
- Java 方法：`getPeriodicalPlanYearList`

## 功能

查询列表。

## 请求

- HTTP 方法：`GET`
- 路径：`/periodical/year/list`
- 方法签名：`R<List<TRecoverPeriodicalPlan>> getPeriodicalPlanYearList(@ApiParam(value = "查询日期（yyyy）不传默认今年", example = "2025") @RequestParam(required = false) String date, @ApiParam(value = "根据儿童姓名模糊查询条件", example = "宏观经济") @RequestParam(required = false) String childName)`

### 参数

- 请求参数：`(value = "查询日期（yyyy）不传默认今年"`
- Query 参数：`example = "2025") String date`
- 请求参数：`(value = "根据儿童姓名模糊查询条件"`
- Query 参数：`example = "宏观经济") String childName`

## 响应

- 声明返回类型：`R<List<TRecoverPeriodicalPlan>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`periodicalPlanService.getPeriodicalTrainListByYearAndUserIdAndChildName`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
