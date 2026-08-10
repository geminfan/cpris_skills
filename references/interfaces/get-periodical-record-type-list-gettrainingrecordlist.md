# GET /periodical/record/type/list

## 定位

- 模块：`training`
- Controller：`PeriodicalController`
- 源码：`C:\work\javacode\cpris_wxapp\training\src\main\java\com\cpris\controller\PeriodicalController.java:216`
- Java 方法：`getTrainingRecordList`

## 功能

查询列表。

## 请求

- HTTP 方法：`GET`
- 路径：`/periodical/record/type/list`
- 方法签名：`R<List<TrainingRecord>> getTrainingRecordList()`

### 参数

无显式参数

## 响应

- 声明返回类型：`R<List<TrainingRecord>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`trainingRecordService.list`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
