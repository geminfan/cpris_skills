# CPRIS Skills

cpris_wxapp 对应的通用 AI 技能，入口为仓库根目录 [SKILL.md](SKILL.md)。提供 REST 接口资料和基于 Python 标准库的 AI 网关客户端，无需 Hermes 或特定 SDK。

## 接入

将本目录完整复制或挂载到智能体支持的技能目录，安装目录命名为 cpris-skills，保留 scripts、references 和可选 agents 元数据。技能发现方式由各智能体运行器决定。

不支持自动发现 SKILL.md 的智能体，可以读取入口作为工具使用说明，通过其终端工具执行 scripts/cpris_auth.py。只有 HTTP 工具的智能体按 [网关契约](references/gateway-contract.md) 请求相同接口；本仓库不是 MCP 服务。

~~~text
使用 cpris-skills 查询儿童列表，默认测试环境。
使用 cpris-skills 解释 /training/list 的参数，不调用接口。
~~~

## 环境与使用

| 环境 | AI 网关 | 业务网关（仅服务端） |
|---|---|---|
| test，当前默认 | http://testai.cpris.com | http://test.cpris.com |
| production，显式切换 | https://aiskills.cpris.com | https://teacherwx.cpris.com |

地址和映射维护在 [gateway-config.json](references/gateway-config.json)。客户端仅请求 AI 网关；部署时还需配置服务端认证和业务转发地址，见 [运行时配置](references/runtime-configuration.md)。

在本目录执行，需要 Python 3.9+，Windows/macOS/Linux 共用：

~~~bash
python scripts/cpris_auth.py login
python scripts/cpris_auth.py call GET /user/info
python scripts/cpris_auth.py call GET /training/list --query date=2026-09-03
python scripts/cpris_auth.py --env production login
python scripts/cpris_auth.py --env production call GET /user/info
~~~

login 隐藏输入并在验证成功后保存。自动化优先由密钥管理器注入 CPRIS_TEST_API_KEY 或 CPRIS_PRODUCTION_API_KEY；只验证使用 login --no-save。

stdout 输出 JSON；退出码 0 成功、1 请求或业务失败、2 配置/输入/本地处理失败。无效命令行由 argparse 输出帮助至 stderr 并返回 2。

## GitHub 公开提交范围

本仓库根目录就是可安装的技能包。提交以下文件，保持相对目录结构：

| 文件或目录 | 是否提交 | 用途 |
|---|---|---|
| SKILL.md | 必须 | 智能体发现技能和读取调用说明的入口 |
| scripts/cpris_auth.py | 必须 | 通用网关调用客户端 |
| references/ | 必须 | 网关配置、调用契约、参数说明与按需加载的接口资料 |
| agents/openai.yaml | 建议保留 | 支持该元数据的智能体展示名称及默认提示；其他智能体可忽略 |
| README.md | 应提交 | GitHub 展示、安装与维护说明 |
| .gitignore | 应提交 | 防止本地凭据、缓存与临时数据被误提交 |

references/gateway-config.json 只有公开网关地址和路由规则，不包含密钥，是客户端运行必需文件。不要笼统忽略所有 JSON 或 Markdown 文件。

不提交实际 API-Key、.env、本地 credentials.json、私钥、虚拟环境、Python 缓存、IDE 配置、日志、临时请求/响应数据。已在 .gitignore 中配置常见规则；临时业务数据统一放在 local/，不要放入 references/。后端 Java 工程、数据库备份和用户数据也不属于本技能仓库。

接口资料由智能体按任务需要读取，无需每次加载整个 references/。部分禁止调用的接口资料用于说明边界，不能仅用 .gitignore 隐藏已被索引引用的文件。

.gitignore 只影响尚未跟踪文件的默认添加行为，不删除已提交文件或 Git 历史，也不是智能体的上下文过滤器。曾经跟踪的文件要停止发布，需要单独取消跟踪；仓库内部 .git/ 是 Git 自身元数据，无需添加到提交清单。

在本仓库目录内，可按上述范围暂存本次修改，再自行提交和推送：

~~~bash
git add .gitignore README.md SKILL.md agents/openai.yaml scripts/cpris_auth.py references/
~~~

## 旧版迁移

- 不自动读取 Hermes 旧 credentials.json。请在目标环境重新 login，防止将旧密钥发送到不同环境；原凭据保留，由用户自行清理。
- CPRIS_AI_GATEWAY 继续支持，但只接受上述两套 AI 地址，并须与所选环境一致；凭据文件不再决定目标网关。
- login 不再接受明文密钥位置参数，改为隐藏输入、环境变量或 --key-stdin。
- 401 不自动清除凭据，因为网关也会透传下游 401。logout 仅清除当前环境本地文件，不撤销服务端密钥。
- ACL 的 403/405/429 不再视为验证成功。完整网关路径也检查删除禁令与业务前缀，不能绕过短路径约束。

## 资料边界

儿童姓名（含昵称、曾用名及对应拼音）和教师姓名（含对应拼音）按 AI 网关成功响应原文直接显示，技能和调用脚本不再额外遮盖。家长姓名及证件、电话、邮箱、住址等仍按网关规则处理；姓名字段中的手机号、证件号和邮箱仍会脱敏。若部署中的后端已返回遮盖内容，技能不猜测或还原。

保留原有 179 项 Controller 映射资料，修订路径定位、参数分组和调用资格；这是包含 SaaS、删除接口的静态快照，不是当前部署的开放接口数。merchant 虽已配置路由，快照没有其接口详情。

脚本仅支持 JSON 请求/响应。文件上传需要遵循相同网关约束的 multipart 调用方。服务端总开关、ACL、机构/员工权限决定实际可用性；源码已知差异和脱敏边界见 [网关契约](references/gateway-contract.md)。
