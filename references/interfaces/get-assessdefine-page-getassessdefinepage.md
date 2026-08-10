# GET /assessDefine/page

## 定位

- 模块：`assess`
- Controller：`AssessDefineController`
- 源码：`C:\work\javacode\cpris_wxapp\assess\src\main\java\com\cpris\controller\AssessDefineController.java:98`
- Java 方法：`getAssessDefinePage`

## 功能

分页查询。

## 请求

- HTTP 方法：`GET`
- 路径：`/assessDefine/page`
- 方法签名：`R<Page<TAssessDefine>> getAssessDefinePage(@ApiParam(value = "页码", example = "1") @RequestParam(defaultValue = "1") long current, @ApiParam(value = "评估定义类型（1：能力评估量表，2：疗效检测量表,:0：诊断评估量表,4：筛查评估量表，5：行为评估量表，7：感知觉量表，6：其他）") String type, @ApiParam(value = "评估定义名称") String assessDefineName)`

### 参数

- 请求参数：`(value = "页码"`
- Query 参数：`example = "1") long current`
- 请求参数：`(value = "评估定义类型（1：能力评估量表，2：疗效检测量表`
- 请求参数：`:0：诊断评估量表`
- 请求参数：`4：筛查评估量表，5：行为评估量表，7：感知觉量表，6：其他）") String type`
- 请求参数：`String assessDefineName`

## 响应

- 声明返回类型：`R<Page<TAssessDefine>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`bossMerchantSuiteService.getAssessDefineProductIdList`、`assessDefineService.page`

## 使用与安全提示

- 认证、租户与数据权限通常由网关、拦截器或服务层承担；调用前应结合部署配置核实。
- 本文档根据静态源码生成；路径前缀（网关 context-path）和运行时权限策略未在 Controller 注解中展开。
