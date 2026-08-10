# POST /user/update

## 定位

- 模块：`user`
- Controller：`UserController`
- 源码：`C:\work\javacode\cpris_wxapp\user\src\main\java\com\cpris\controller\UserController.java:73`
- Java 方法：`updateUser`

## 功能

POST /user/update。

## 请求

- HTTP 方法：`POST`
- 路径：`/user/update`
- 方法签名：`R<String> updateUser(@RequestBody TEmployee employee)`

### 参数

- 请求体 JSON：`TEmployee employee`

## 响应

- 声明返回类型：`R<String>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`employeeService.updateById`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
