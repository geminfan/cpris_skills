# GET /assess/page

## 定位

- 模块：`assess`
- Controller：`AssessController`
- 源码：`C:\work\javacode\cpris_wxapp\assess\src\main\java\com\cpris\controller\AssessController.java:107`
- Java 方法：`getAssessPage`

## 功能

分页查询。

## 请求

- HTTP 方法：`GET`
- 路径：`/assess/page`
- 方法签名：`R<com.baomidou.mybatisplus.extension.plugins.pagination.Page<VSmdAssess>> getAssessPage(@ApiParam(value = "页码", example = "1") @RequestParam(defaultValue = "1") long current, @ApiParam(value = "儿童姓名", example = "小留学") String childName, @ApiParam(value = "教师用户id", example = "geminfan") String userId, @ApiParam(value = "评估状态(1未评估,2未完成,3已完成)", example = "3") String assessProgress)`

### 参数

- 请求参数：`(value = "页码"`
- Query 参数：`example = "1") long current`
- 请求参数：`(value = "儿童姓名"`
- 请求参数：`example = "小留学") String childName`
- 请求参数：`(value = "教师用户id"`
- 请求参数：`example = "geminfan") String userId`
- 请求参数：`(value = "评估状态(1未评估`
- 请求参数：`2未完成`
- 请求参数：`3已完成)"`
- 请求参数：`example = "3") String assessProgress`

## 响应

- 声明返回类型：`R<com.baomidou.mybatisplus.extension.plugins.pagination.Page<VSmdAssess>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`assessService.getAssessPageByParams`、`assessDefineService.list`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
