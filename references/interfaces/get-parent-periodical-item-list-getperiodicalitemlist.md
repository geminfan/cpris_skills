# GET /parent/periodical/item/list

## 定位

- 模块：`parent`
- Controller：`ParentPeriodicalController`
- 源码：`C:\work\javacode\cpris_wxapp\parent\src\main\java\com\cpris\controller\ParentPeriodicalController.java:156`
- Java 方法：`getPeriodicalItemList`

## 功能

查询列表。

## 请求

- HTTP 方法：`GET`
- 路径：`/parent/periodical/item/list`
- 方法签名：`R<Object> getPeriodicalItemList(@ApiParam(value = "评估定义id", required = true, example = "") @RequestParam String assessDefineId, @ApiParam(value = "儿童id", required = true, example = "") @RequestParam String childId)`

### 参数

- 请求参数：`(value = "评估定义id"`
- 请求参数：`required = true`
- Query 参数：`example = "") String assessDefineId`
- 请求参数：`(value = "儿童id"`
- 请求参数：`required = true`
- Query 参数：`example = "") String childId`

## 响应

- 声明返回类型：`R<Object>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`assessService.getOne`、`assessDefineService.getById`、`dataCacheService.getData`、`teacherGuideService.getTeacherGuideListByAssessIdAndItem`、`pep3TeacherGuideService.getTeacherGuideListByAssessIdAndItem`、`samTeacherGuideService.getTeacherGuideListByAssessIdAndItem`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
