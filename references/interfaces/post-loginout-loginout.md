# POST /loginOut

## 定位

- 模块：`saas`
- Controller：`LoginController`
- 源码：`C:\work\javacode\cpris_wxapp\saas\auth\src\main\java\com\cpris\controller\LoginController.java:113`
- Java 方法：`loginOut`

## 功能

登录。

## 请求

- HTTP 方法：`POST`
- 路径：`/loginOut`
- 方法签名：`R<String> loginOut(@ApiIgnore @RequestHeader(value = "Authorization", required = false) String authorizationHeader)`

### 参数

- 请求头：`(value = "Authorization"`
- 请求参数：`required = false) String authorizationHeader`

## 响应

- 声明返回类型：`R<String>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

未检测到 Service / Mapper / Client 直接调用（可能为本地逻辑或调用名称未遵循约定）。

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
