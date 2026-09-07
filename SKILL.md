---
name: cpris-skills
description: 查询 CPRIS 微信端 REST 接口、解释参数与返回类型，并通过 CPRIS AI 网关执行获授权的儿童、用户、家长、训练和评估业务操作；支持把打印后手写评定的扫描 PDF 或图片导入对应儿童的评估问卷。支持测试与正式环境、API-Key 认证；不提供删除、登录短信或内部换 token 操作。
---

# CPRIS 微信端 REST API

供支持文件技能的 AI 智能体使用，内容和 Python 客户端不依赖特定智能体；agents/openai.yaml 是可选的产品元数据。

## 工作方式

1. 区分接口查询与实际业务操作。仅查文档、解释参数时不读取密钥、不要求登录、不发网络请求。
2. 优先在 `references/interfaces/` 按 HTTP 路径或业务关键词搜索并只读取命中的接口详情；路径不明确时才读取 [接口总览](references/api-overview.md) 和对应模块索引。不要遍历或加载全部接口文档。需要确定请求字段、必填规则、日期格式或构造请求体时，改读 [前端实际调用接口手册](references/app-usage/README.md) 对应模块文档：它按教师端 App 真实调用整理了字段、后端校验与坑，比 interfaces/ 骨架完整，两者冲突时以它为准。
3. 已知方法、路径和参数后直接调用，不为常规调用预先执行 `status`、`health` 或 `login`。仅在缺少凭据时处理登录，连接异常时才用 `health` 区分网关状态，401 时才重新验证密钥。
4. 默认测试环境；只有用户或现有运行配置明确选择 production 时才传 `--env production`。环境、凭据或部署细节存在疑问时再读取 [运行时配置](references/runtime-configuration.md)，不能因测试失败而切换正式环境。
5. 使用 `scripts/cpris_auth.py call`，或按 [网关契约](references/gateway-contract.md) 执行等价请求。脚本已经执行环境、路由、删除禁令、HTTP 状态和业务 code 检查；只有解释这些规则、处理特殊响应或缺少 Python 时才读取网关契约和 [请求与响应约定](references/schemas.md)。
6. 仅交付成功响应中的数据，按网关返回值展示。网关根据 API-Key 绑定账号的 ai_show 权限逐项决定是否脱敏；已授权返回的原文不额外遮盖，已遮盖内容不猜测或还原。
7. 调用失败、网关报错或环境异常（例如机器没有 Python）时，先读取 [已知问题与规避](references/known-issues.md) 按既有方案处理，减少重复排查和调用耗时；新问题解决后把「日期、现象、原因、规避」追加到该文件末尾，避免其他智能体重复踩坑。Windows 无 Python 时用 `scripts/cpris_call.ps1` 执行等价调用。

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

无 Python 的 Windows 机器可用 PowerShell 等价客户端 `scripts/cpris_call.ps1`：

~~~bash
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cpris_call.ps1 -Method GET -Path /childrenInfo/page -Query current=1
~~~

密钥同样从凭据文件或环境变量读取；中文查询值用 `-QueryFile`（UTF-8 文本，每行 key=value），中文 JSON 正文用 `-BodyFile`（UTF-8 文件），不要把中文放进命令行参数。输出首行为 `HTTP_STATUS:<code>`，其后为响应原文；智能体须确认 HTTP 2xx、响应为 JSON 且存在的业务 code=200 后才交付数据，不展示错误或非 JSON 原文。成功数据按网关返回值展示，不另做脱敏。

## 操作边界

- 仅执行用户已经授权的操作。创建、更新、保存、绑定等按实际副作用判断，不能仅根据 GET/POST 判断只读。现有明确授权已覆盖的操作无需重复确认。
- 新建或更新评估时，不能只提交 `childId`、`assessDefineId` 和审计字段。必须同时提交 `assessDate`、`assessAppointDate`、`employeeId` 和 `assessType`（服务端按显式白名单落库，`assessAppointDate` 会被置为 `assessDate`，修改时也不能更换 childId）；`realAssessPerson` 不经该接口写入，由完成/生成类操作自动记录当前用户。`dgCreatedDate`、`dgCreatedBy` 仅是审计字段，不能替代评估时间或评估老师。C-PEP-3 等能力评估使用 `assessType: "1"`，评估老师账号填入 `employeeId`。字段级细节见 [评估模块手册](references/app-usage/assess.md)。
- 新建儿童（`POST /childrenInfo/saveOrUpdate`，无 childId 即新建）时必须携带接待日期：请求体包含 `childrenVisitList: [{"jdrq": "<接待日期>"}]`，用户未指定时默认当前时间（ISO-8601 字符串或毫秒时间戳）。服务端只在 childrenVisitList 非空时写入 `t_children_visit`，不带则儿童没有接待记录和接待日期。更新已有儿童的 `childrenVisitList`/`childrenGuardianList` 是先删后插，必须传完整列表，禁止传 `[null]` 或残缺数据。
- 网关禁止 DELETE 和删除路径，包括 POST /assess/delete 等。不得换方法、借用路由、编码或直连业务服务绕过。
- 登录、短信、SaaS 数据/文件及内部 /ai/key/token、/ai/permissions 不在技能调用范围，完整网关路径也必须检查真实业务路径。token 获取和权限查询由网关处理，技能只携带 X-Api-Key 调用业务接口。
- 不自动重试写操作；超时不代表服务端未完成，不通过改用其他 HTTP 方法规避 405。
- health 不证明密钥有效；403、405、429 可能发生在 auth 验证之前，不能据此宣布登录成功。
- 教师姓名、身份证、手机号、邮箱、地址，以及儿童姓名、身份证、联系方式、家庭住址，分别受 ai_skill_manage 下对应 ai_show 权限控制，权限对照见 [网关契约](references/gateway-contract.md)。无对应权限或权限查询失败时，网关保持对应字段脱敏。技能不自行推断、授予或缓存显示权限，也不把已脱敏响应判为调用失败或尝试绕过网关获取原文。错误和非 JSON 响应仍不展示原文；不能宣称所有响应均保证脱敏。
- 接口详情源码位置以 cpris_wxapp/ 开头；只有需要追踪且环境有源码时才读取。缺少源码时说明资料边界，不要求使用者安装后端工程。

## 按需参考

- [前端实际调用接口手册（字段、必填、格式、后端约束与坑）](references/app-usage/README.md)
- [配置、凭据与多智能体接入](references/runtime-configuration.md)
- [路由、鉴权、删除禁令与错误处理](references/gateway-contract.md)
- [参数绑定与请求响应](references/schemas.md)
- [模块与接口目录](references/api-overview.md)
- [扫描 PDF 或图片中的纸质评估结果并导入](references/assessment-form-import.md)
- [历史踩坑与规避方案](references/known-issues.md)
