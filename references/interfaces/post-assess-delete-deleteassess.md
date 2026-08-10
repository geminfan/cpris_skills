# POST /assess/delete

## 定位

- 模块：`assess`
- Controller：`AssessController`
- 源码：`C:\work\javacode\cpris_wxapp\assess\src\main\java\com\cpris\controller\AssessController.java:937`
- Java 方法：`deleteAssess`

## 功能

删除。

## 请求

- HTTP 方法：`POST`
- 路径：`/assess/delete`
- 方法签名：`R<String> deleteAssess(@RequestBody AssessVo assessVo)`

### 参数

- 请求体 JSON：`AssessVo assessVo`

## 响应

- 声明返回类型：`R<String>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`assessResultValueService.remove`、`assessService.remove`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
