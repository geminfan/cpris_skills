# GET /files/signature/{merchantId}/{uuid}/{fileName}/{ticket}

## 定位

- 模块：`saas`
- Controller：`DataController`
- 源码：`C:\work\javacode\cpris_wxapp\saas\auth\src\main\java\com\cpris\controller\DataController.java:136`
- Java 方法：`getSignatureImage`

## 功能

GET /files/signature/{merchantId}/{uuid}/{fileName}/{ticket}。

## 请求

- HTTP 方法：`GET`
- 路径：`/files/signature/{merchantId}/{uuid}/{fileName}/{ticket}`
- 方法签名：`ResponseEntity<Object> getSignatureImage(@PathVariable String merchantId, @PathVariable String uuid, @PathVariable String fileName, @PathVariable(required = false) String ticket)`

### 参数

- 路径参数：`String merchantId`
- 路径参数：`String uuid`
- 路径参数：`String fileName`
- 路径参数：`String ticket`

## 响应

- 声明返回类型：`ResponseEntity<Object>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`fileTicketService.getById`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
