# GET /childrenInfo/region/list

## 定位

- 模块：`children`
- Controller：`ChildrenInfoController`
- 源码：`C:\work\javacode\cpris_wxapp\children\src\main\java\com\cpris\controller\ChildrenInfoController.java:200`
- Java 方法：`getRegionList`

## 功能

查询列表。

## 请求

- HTTP 方法：`GET`
- 路径：`/childrenInfo/region/list`
- 方法签名：`R<List<TRegion>> getRegionList(@ApiParam(value = "上级id 例如(广东省的regionId=20 查询广东省下面的市就传parentId=20),传1就是查省级", example = "上级id 例如(广东省的regionId=20 查询广东省下面的市就传parentId=20),传1就是查省级") @RequestParam(defaultValue = "1") String parentId)`

### 参数

- 请求参数：``
- 请求参数：`传1就是查省级"`
- 请求参数：`example = "上级id 例如(广东省的regionId=20 查询广东省下面的市就传parentId=20)`
- Query 参数：`传1就是查省级") String parentId`

## 响应

- 声明返回类型：`R<List<TRegion>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`regionService.list`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
