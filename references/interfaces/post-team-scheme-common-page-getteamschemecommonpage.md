# POST /team/scheme/common/page

## 定位

- 模块：`training`
- Controller：`TeamController`
- 源码：`C:\work\javacode\cpris_wxapp\training\src\main\java\com\cpris\controller\TeamController.java:221`
- Java 方法：`getTeamSchemeCommonPage`

## 功能

分页查询。

## 请求

- HTTP 方法：`POST`
- 路径：`/team/scheme/common/page`
- 方法签名：`R<Page<VSmdCourseScheme>> getTeamSchemeCommonPage(@ApiParam(value = "页码", example = "1") @RequestParam(defaultValue = "1") long current, @RequestBody SchemeVo schemeVo)`

### 参数

- 请求参数：`(value = "页码"`
- Query 参数：`example = "1") long current`
- 请求体 JSON：`SchemeVo schemeVo`

## 响应

- 声明返回类型：`R<Page<VSmdCourseScheme>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`schemeService.getSchemeCommonPage`、`sysBasedataService.list`、`dataCacheService.getData`、`groupService.list`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
