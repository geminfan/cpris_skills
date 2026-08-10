# GET /parent/team/lesson/info

## 定位

- 模块：`parent`
- Controller：`ParentTeamController`
- 源码：`C:\work\javacode\cpris_wxapp\parent\src\main\java\com\cpris\controller\ParentTeamController.java:109`
- Java 方法：`getTeamLessonInfo`

## 功能

查询详情。

## 请求

- HTTP 方法：`GET`
- 路径：`/parent/team/lesson/info`
- 方法签名：`R<TStratoScheduleDefine> getTeamLessonInfo(@ApiParam(value = "组训课程id", required = true) @RequestParam String scheduleDefineId)`

### 参数

- 请求参数：`(value = "组训课程id"`
- Query 参数：`required = true) String scheduleDefineId`

## 响应

- 声明返回类型：`R<TStratoScheduleDefine>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`scheduleDefineService.getTeamLessonInfoById`、`signatureDataService.getImagePath`、`fileTicketService.generateTicket`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
