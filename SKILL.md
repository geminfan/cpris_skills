---
name: cpris-wxapp-rest-api
description: 查询 CPRIS 微信端 REST 接口、解释参数与返回类型，并通过 CPRIS AI 网关执行获授权的儿童、用户、家长、训练和评估业务操作。支持测试与正式环境、API-Key 认证；不提供删除、登录短信或内部换 token 操作。
---

# CPRIS 微信端 REST API

供支持文件技能的 AI 智能体使用，内容和 Python 客户端不依赖特定智能体；agents/openai.yaml 是可选的产品元数据。

## 工作方式

1. 区分接口查询与实际业务操作。仅查文档、解释参数时不读取密钥、不要求登录、不发网络请求。
2. 从 [接口总览](references/api-overview.md) 进入相关模块和接口详情，核对方法、路径、参数与调用资格。索引包含不可调用的历史接口，收录不等于开放。
3. 实际请求前读取 [运行时配置](references/runtime-configuration.md)。默认测试环境；正式环境必须由用户或运行配置明确选择，不能因测试失败而切换正式环境。
4. 使用 scripts/cpris_auth.py，或按 [网关契约](references/gateway-contract.md) 执行等价 HTTP 请求。路径为 /ai/gw/{service}/{业务路径}，仅使用 X-Api-Key 认证，不直连业务网关、不自行获取 JWT。
5. 根据 [请求与响应约定](references/schemas.md) 检查 HTTP 状态和业务 code。仅交付成功响应中的数据；儿童、教师姓名按返回原文直接显示，不做额外脱敏，不猜测被遮盖内容。

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

login 隐藏输入密钥；无交互智能体优先由密钥管理器注入 CPRIS_TEST_API_KEY 或 CPRIS_PRODUCTION_API_KEY，也可使用 login --key-stdin。不要把密钥写在命令参数、脚本或对话回复里。仅验证时加 --no-save；环境密钥可直接用于 call，不要求先持久化。

## 操作边界

- 仅执行用户已经授权的操作。创建、更新、保存、绑定等按实际副作用判断，不能仅根据 GET/POST 判断只读。现有明确授权已覆盖的操作无需重复确认。
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
