# GET /sysBasedata/list

## 定位

- 模块：`saas`
- Controller：`DataController`
- 源码：`C:\work\javacode\cpris_wxapp\saas\auth\src\main\java\com\cpris\controller\DataController.java:105`
- Java 方法：`getKinshipList`

## 功能

查询列表。

## 请求

- HTTP 方法：`GET`
- 路径：`/sysBasedata/list`
- 方法签名：`R<Map<String, List<SysBasedata>>> getKinshipList(@ApiParam(value = "数据字典类型代码列表", required = true) @RequestParam List<String> dataTypes)`

### 参数

- 请求参数：`(value = "数据字典类型代码列表"`
- Query 参数：`required = true) List<String> dataTypes`

## 响应

- 声明返回类型：`R<Map<String, List<SysBasedata>>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`sysBasedataService.list`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
