# GET /team/dateRange/page

## 定位

- 模块：`training`
- Controller：`TeamController`
- 源码：`C:\work\javacode\cpris_wxapp\training\src\main\java\com\cpris\controller\TeamController.java:783`
- Java 方法：`getLessonDateRangePage`

## 功能

分页查询。

## 请求

- HTTP 方法：`GET`
- 路径：`/team/dateRange/page`
- 方法签名：`R<Page<TStratoScheduleDefine>> getLessonDateRangePage(@ApiParam(value = "页码", example = "1") @RequestParam(defaultValue = "1") long current, @ApiParam(value = "查询开始日期（yyyy-MM-dd）,不传默认当前一周时间", example = "2026-07-13") @RequestParam(required = false) String startDate, @ApiParam(value = "查询截止日期（yyyy-MM-dd）,不传默认当前一周时间", example = "2026-07-19") @RequestParam(required = false) String endDate, @ApiParam(value = "小组id查询参数", example = "5") @RequestParam(required = false) String groupId, @ApiParam(value = "儿童姓名", example = "小章") @RequestParam(required = false) String childName)`

### 参数

- 请求参数：`(value = "页码"`
- Query 参数：`example = "1") long current`
- 请求参数：`(value = "查询开始日期（yyyy-MM-dd）`
- 请求参数：`不传默认当前一周时间"`
- Query 参数：`example = "2026-07-13") String startDate`
- 请求参数：`(value = "查询截止日期（yyyy-MM-dd）`
- 请求参数：`不传默认当前一周时间"`
- Query 参数：`example = "2026-07-19") String endDate`
- 请求参数：`(value = "小组id查询参数"`
- Query 参数：`example = "5") String groupId`
- 请求参数：`(value = "儿童姓名"`
- Query 参数：`example = "小章") String childName`

## 响应

- 声明返回类型：`R<Page<TStratoScheduleDefine>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`childrenInfoService.list`、`recoverProcessGroupService.list`、`scheduleDefineService.getTeamTrainPageByDayRangeAndUserIdAndParticipantIds`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
