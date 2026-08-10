# POST /parent/wx/login

## 定位

- 模块：`saas`
- Controller：`ParentLoginController`
- 源码：`C:\work\javacode\cpris_wxapp\saas\auth\src\main\java\com\cpris\controller\ParentLoginController.java:44`
- Java 方法：`wxLogin`

## 功能

登录。

## 请求

- HTTP 方法：`POST`
- 路径：`/parent/wx/login`
- 方法签名：`R<AccessToken> wxLogin(@ApiParam(value = "页码", example = "1") @RequestParam(defaultValue = "1") long current, @ApiParam(value = "儿童姓名") String name, @ApiParam(value = "儿童状态(2已登记 5已入训 9已离训)") String status)`

### 参数

- 请求参数：`(value = "页码"`
- Query 参数：`example = "1") long current`
- 请求参数：`String name`
- 请求参数：`") String status`

## 响应

- 声明返回类型：`R<AccessToken>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

未检测到 Service / Mapper / Client 直接调用（可能为本地逻辑或调用名称未遵循约定）。

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
