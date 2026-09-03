# GET /assess/page

## 定位

- 模块：`assess`
- Controller：`AssessController`
- 源码：`cpris_wxapp/assess/src/main/java/com/cpris/controller/AssessController.java:107`
- Java 方法：`getAssessPage`

## 功能

分页查询。

## 请求

- HTTP 方法：`GET`
- 路径：`/assess/page`
- 方法签名：`R<com.baomidou.mybatisplus.extension.plugins.pagination.Page<VSmdAssess>> getAssessPage(@ApiParam(value = "页码", example = "1") @RequestParam(defaultValue = "1") long current, @ApiParam(value = "儿童姓名", example = "小留学") String childName, @ApiParam(value = "教师用户id", example = "geminfan") String userId, @ApiParam(value = "评估状态(1未评估,2未完成,3已完成)", example = "3") String assessProgress)`

### 参数

- Query/表单：`@ApiParam(value = "页码", example = "1") @RequestParam(defaultValue = "1") long current`
- Spring MVC 默认绑定：`@ApiParam(value = "儿童姓名", example = "小留学") String childName`
- Spring MVC 默认绑定：`@ApiParam(value = "教师用户id", example = "geminfan") String userId`
- Spring MVC 默认绑定：`@ApiParam(value = "评估状态(1未评估,2未完成,3已完成)", example = "3") String assessProgress`

## 响应

- 声明返回类型：`R<com.baomidou.mybatisplus.extension.plugins.pagination.Page<VSmdAssess>>`
- 实际字段结构应以返回 DTO / VO 类型和公共响应包装类的定义为准。

## 调用链

`assessService.getAssessPageByParams`、`assessDefineService.list`

## 使用与安全提示

- AI 调用：经 AI 网关调用，受用户授权与运行时权限约束。
- 实际请求必须使用 AI 网关及 X-Api-Key；完整路径也不能绕过禁令，见 [网关契约](../gateway-contract.md)。
- 参数按完整 Java 参数分组并保留注解；DTO 字段与绑定规则见 [请求与响应约定](../schemas.md)。
- 源码路径相对于 cpris_wxapp 所在目录；行号与调用链为静态快照，收录不代表当前部署已开放。
