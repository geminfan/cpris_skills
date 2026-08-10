# GET /childrenInfo/page

## 定位

- 模块：`children`
- Controller：`ChildrenInfoController`
- 源码：`C:\work\javacode\cpris_wxapp\children\src\main\java\com\cpris\controller\ChildrenInfoController.java:61`
- Java 方法：`getChildrenInfoPage`

## 功能

分页查询。

## 请求

- HTTP 方法：`GET`
- 路径：`/childrenInfo/page`
- 方法签名：`R<Page<TChildrenInfo>> getChildrenInfoPage(@ApiParam(value = "页码", example = "1") @RequestParam(defaultValue = "1") long current, @ApiParam(value = "儿童姓名") String name, @ApiParam(value = "儿童状态(2已登记 5已入训 9已离训)") String status)`

### 参数

- 请求参数：`(value = "页码"`
- Query 参数：`example = "1") long current`
- 请求参数：`String name`
- 请求参数：`") String status`

## 响应

- 声明返回类型：`R<Page<TChildrenInfo>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`childrenInfoService.page`、`recoverProcessService.list`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
