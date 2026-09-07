# 请求与响应约定

## 路径和参数

详情记录业务路径，调用时按 [网关契约](gateway-contract.md) 添加 /ai/gw/{service}，环境由运行配置选择。

- @RequestBody：JSON 请求体；字段取决于 DTO/VO/Entity，不从类型名猜测。
- @RequestParam：Query 或表单参数；name/value 为外部名称，required/defaultValue 影响必填规则。参考完整注解。
- @PathVariable：替换路径模板变量并编码，不将花括号占位符直接发给服务端。
- @RequestHeader：请求头参数；客户端身份仍仅使用 X-Api-Key，不手动传 Authorization 或方法覆盖头。
- 无绑定注解：基础类型通常绑定 Query/表单，对象按 Spring MVC model attribute 处理，受实际部署设置影响。
- MultipartFile：文件上传，不是 JSON。当前脚本不支持 multipart，专用调用方仍必须经过 AI 网关。
- @ApiParam 是文档注解，不是独立业务参数；不能把注解内的逗号拆成多个参数。

参数分组来自快照完整方法签名，不是 DTO 的完整字段 schema。必填性或字段含义缺失时根据签名及可用源码判断，没有材料则说明缺失。例如 /training/list 的必填参数为 date（yyyy-MM-dd），不是 page/size。

## Python 脚本输出

stdout 为 JSON，成功示例：

~~~json
{"ok":true,"httpStatus":200,"data":{"code":200,"msg":"成功","data":{}}}
~~~

外层 data 保留后端 JSON 包装，内层 data 才是 R<T> 业务对象。静态 Java 类型不是完整的运行时 JSON schema。

失败示例：

~~~json
{"ok":false,"httpStatus":200,"businessCode":502,"error":"业务返回失败；HTTP 成功不代表业务成功。"}
~~~

- 退出码 0 成功、1 请求/业务失败、2 配置/输入/本地处理失败。
- status 只说明本地配置，health 只说明网关响应，都不代表业务权限。
- 正常调用检查 HTTP 2xx 与存在的 code=200；login 还要求 code=200、data 为非空用户对象。
- 错误说明由客户端生成，不将原始下游错误数据作为可交付业务数据展示。
- 非 JSON 内容、文件下载和 HEAD 等无 JSON 响应不作为可展示业务数据输出。
- 正常 JSON 按网关返回值展示：姓名、证件、电话、邮箱、地址由账号对应 ai_show 权限决定是否显示原文。客户端不额外遮盖获授权原文，不猜测或还原已遮盖内容；脱敏结果本身不表示调用失败。权限映射、字段识别及部署限制见 [网关契约](gateway-contract.md)。

## PowerShell 备用脚本输出

脚本输出 HTTP_STATUS:<code> 后跟响应原文，退出码只反映 HTTP 状态。智能体须自行确认 HTTP 2xx、响应为 JSON 且存在的业务 code=200 后才交付数据；错误与非 JSON 原文不展示。成功字段同样按网关返回值展示，脚本不额外查询或缓存显示权限。
