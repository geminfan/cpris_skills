# GET /assess/result/status/map

## 定位

- 模块：`assess`
- Controller：`AssessController`
- 源码：`C:\work\javacode\cpris_wxapp\assess\src\main\java\com\cpris\controller\AssessController.java:884`
- Java 方法：`getAssessPaperResultStatus`

## 功能

GET /assess/result/status/map。

## 请求

- HTTP 方法：`GET`
- 路径：`/assess/result/status/map`
- 方法签名：`R<Map<String, String>> getAssessPaperResultStatus(@RequestParam String assessId)`

### 参数

- Query 参数：`String assessId`

## 响应

- 声明返回类型：`R<Map<String, String>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`assessResultValueService.list`、`assessDefinePaperService.getById`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
