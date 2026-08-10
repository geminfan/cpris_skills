# GET /parent/periodical/record/list

## 定位

- 模块：`parent`
- Controller：`ParentPeriodicalController`
- 源码：`C:\work\javacode\cpris_wxapp\parent\src\main\java\com\cpris\controller\ParentPeriodicalController.java:111`
- Java 方法：`getRecordList`

## 功能

查询列表。

## 请求

- HTTP 方法：`GET`
- 路径：`/parent/periodical/record/list`
- 方法签名：`R<List<TRecoverLessonRecord>> getRecordList(@ApiParam(value = "个训计划id", required = true) @RequestParam String planId)`

### 参数

- 请求参数：`(value = "个训计划id"`
- Query 参数：`required = true) String planId`

## 响应

- 声明返回类型：`R<List<TRecoverLessonRecord>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`periodicalPlanDetailService.list`、`recordService.list`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
