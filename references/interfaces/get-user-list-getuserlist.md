# GET /user/list

## 定位

- 模块：`user`
- Controller：`UserController`
- 源码：`C:\work\javacode\cpris_wxapp\user\src\main\java\com\cpris\controller\UserController.java:45`
- Java 方法：`getUserList`

## 功能

查询列表。

## 请求

- HTTP 方法：`GET`
- 路径：`/user/list`
- 方法签名：`R<List<TEmployee>> getUserList(@ApiParam(value = "用户名称", example = "小留学") String name, @ApiParam(value = "用户状态", example = "1") String status)`

### 参数

- 请求参数：`(value = "用户名称"`
- 请求参数：`example = "小留学") String name`
- 请求参数：`(value = "用户状态"`
- 请求参数：`example = "1") String status`

## 响应

- 声明返回类型：`R<List<TEmployee>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`employeeService.list`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
