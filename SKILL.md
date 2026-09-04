---
name: cpris-skills
description: 查询 CPRIS 微信端 REST 接口、解释参数与返回类型，并通过 CPRIS AI 网关执行获授权的儿童、用户、家长、训练和评估业务操作；支持把打印后手写评定的扫描 PDF 或图片导入对应儿童的评估问卷。支持测试与正式环境、API-Key 认证；不提供删除、登录短信或内部换 token 操作。
---

# CPRIS 微信端 REST API

供支持文件技能的 AI 智能体使用，内容和 Python 客户端不依赖特定智能体；agents/openai.yaml 是可选的产品元数据。

## 工作方式

1. 区分接口查询与实际业务操作。仅查文档、解释参数时不读取密钥、不要求登录、不发网络请求。
2. 优先在 `references/interfaces/` 按 HTTP 路径或业务关键词搜索并只读取命中的接口详情；路径不明确时才读取 [接口总览](references/api-overview.md) 和对应模块索引。不要遍历或加载全部接口文档。
3. 已知方法、路径和参数后直接调用，不为常规调用预先执行 `status`、`health` 或 `login`。仅在缺少凭据时处理登录，连接异常时才用 `health` 区分网关状态，401 时才重新验证密钥。
4. 默认测试环境；只有用户或现有运行配置明确选择 production 时才传 `--env production`。环境、凭据或部署细节存在疑问时再读取 [运行时配置](references/runtime-configuration.md)，不能因测试失败而切换正式环境。
5. 使用 `scripts/cpris_auth.py call`，或按 [网关契约](references/gateway-contract.md) 执行等价请求。脚本已经执行环境、路由、删除禁令、HTTP 状态和业务 code 检查；只有解释这些规则、处理特殊响应或缺少 Python 时才读取网关契约和 [请求与响应约定](references/schemas.md)。
6. 仅交付成功响应中的数据；儿童、教师姓名按返回原文直接显示，不做额外脱敏，不猜测被遮盖内容。

## 纸质评估导入

用户上传打印后手写填写的评估问卷 PDF 或一组图片，并要求把勾选、评分或填空导入 CPRIS 时，读取并遵循 [扫描评估问卷导入](references/assessment-form-import.md)。该流程用于更新已有儿童的已有评估；创建儿童、创建评估或补写附件中没有的信息仍需用户明确授权。

## 环境

| 环境 | AI 网关：智能体请求目标 | 业务网关：仅服务端转发 |
|---|---|---|
| test（默认） | http://testai.cpris.com | http://test.cpris.com |
| production | https://aiskills.cpris.com | https://teacherwx.cpris.com |

地址及路由集中在 [gateway-config.json](references/gateway-config.json)。密钥绑定目标网关，测试密钥不自动复用到正式环境。

## 调用

以下命令相对于已安装技能目录；从其他目录执行时使用脚本绝对路径。需要 Python 3.9+，无第三方依赖。

~~~bash
python scripts/cpris_auth.py status
python scripts/cpris_auth.py health
python scripts/cpris_auth.py login
python scripts/cpris_auth.py call GET /user/info
python scripts/cpris_auth.py call GET /childrenInfo/page --query current=1
python scripts/cpris_auth.py call GET /training/list --query date=2026-09-03
python scripts/cpris_auth.py --env production login
python scripts/cpris_auth.py --env production call GET /user/info
~~~

`call` 是已有凭据时的快速路径。login 隐藏输入密钥；无交互智能体优先由密钥管理器注入 CPRIS_TEST_API_KEY 或 CPRIS_PRODUCTION_API_KEY，也可使用 login --key-stdin。不要把密钥写在命令参数、脚本或对话回复里。仅验证时加 --no-save；环境密钥可直接用于 call，不要求先持久化。

## 操作边界

- 仅执行用户已经授权的操作。创建、更新、保存、绑定等按实际副作用判断，不能仅根据 GET/POST 判断只读。现有明确授权已覆盖的操作无需重复确认。
- 新建或更新评估时，不能只提交 `childId`、`assessDefineId` 和审计字段。必须按原系统业务记录同时写入 `assessDate`、`assessAppointDate`、`realAssessPerson`、`employeeId` 和 `assessType`；`dgCreatedDate`、`dgCreatedBy` 仅是审计字段，不能替代评估时间或评估老师。C-PEP-3 等能力评估使用 `assessType: "1"`，评估老师账号应同时填入 `realAssessPerson` 和 `employeeId`。
- 网关禁止 DELETE 和删除路径，包括 POST /assess/delete 等。不得换方法、借用路由、编码或直连业务服务绕过。
- 登录、短信、SaaS 数据/文件与 /ai/key/token 不在技能调用范围，完整网关路径也必须检查真实业务路径。
- 不自动重试写操作；超时不代表服务端未完成，不通过改用其他 HTTP 方法规避 405。
- health 不证明密钥有效；403、405、429 可能发生在 auth 验证之前，不能据此宣布登录成功。
- 儿童姓名（含昵称、曾用名及对应拼音）和教师姓名（含对应拼音）按成功响应原文直接显示，不做额外脱敏；姓名字段中的手机号、证件号和邮箱仍执行内容脱敏，其他敏感字段保持脱敏形态。若后端已遮盖姓名，不猜测或还原。当前后端部分错误和非 JSON 响应直接透传，脚本不输出这类原文；不能宣称所有响应均保证脱敏。
- 接口详情源码位置以 cpris_wxapp/ 开头；只有需要追踪且环境有源码时才读取。缺少源码时说明资料边界，不要求使用者安装后端工程。

## 按需参考

- [配置、凭据与多智能体接入](references/runtime-configuration.md)
- [路由、鉴权、删除禁令与错误处理](references/gateway-contract.md)
- [参数绑定与请求响应](references/schemas.md)
- [模块与接口目录](references/api-overview.md)
- [扫描 PDF 或图片中的纸质评估结果并导入](references/assessment-form-import.md)
