# 运行时配置

## 环境选择

唯一机器配置源为 [gateway-config.json](gateway-config.json)：

| 环境 | AI 网关 | 业务网关（仅服务端） |
|---|---|---|
| test（默认） | http://testai.cpris.com | http://test.cpris.com |
| production | https://aiskills.cpris.com | https://teacherwx.cpris.com |

- 环境优先级：--env > CPRIS_ENV > 默认 test。
- 地址优先级：--gateway > CPRIS_AI_GATEWAY > 所选环境的 aiGateway。
- 地址覆盖只接受配置中的两套 AI 地址。只提供地址时推导环境；同时提供环境但地址不匹配时拒绝。允许地址末尾斜杠。
- 凭据文件仅校验 environment/gateway 绑定，不参与选择环境。
- businessGateway 是部署参考；客户端不将它作为请求地址，也不接受任意 URL、业务端口或跟随重定向。
- 默认超时 30 秒，全局 --timeout 可设置为不超过 300 秒；无自动重试。

全局选项须位于子命令之前：

~~~bash
python scripts/cpris_auth.py --env test health
python scripts/cpris_auth.py --env production status
python scripts/cpris_auth.py --gateway https://aiskills.cpris.com call GET /user/info
~~~

## 凭据来源

每次业务调用按顺序读取：

1. 当前环境的 CPRIS_TEST_API_KEY 或 CPRIS_PRODUCTION_API_KEY。
2. CPRIS_API_KEY，但同时要求 CPRIS_API_KEY_GATEWAY 与当前 AI 网关一致。
3. 当前环境本地 credentials.json。

通过智能体或宿主密钥管理器提供环境变量。密钥不放入命令参数、文档、版本库、日志或回复；HTTP 只使用 X-Api-Key。JWT 完全由网关内部获取，不由客户端保存。

| 条件 | 凭据根目录 |
|---|---|
| 显式配置 | CPRIS_CONFIG_HOME：工作区/仓库之外的绝对路径 |
| Windows | %APPDATA%/cpris；APPDATA 未设置时为用户 AppData/Roaming/cpris |
| macOS/Linux | XDG_CONFIG_HOME 下的 cpris；未设置时为 ~/.config/cpris |

根目录下按 cpris-wxapp-rest-api/test/credentials.json 和 cpris-wxapp-rest-api/production/credentials.json 隔离。

保存字段为 environment、gateway、validatedAt，以及密钥字段。POSIX 使用 apiKey，目录 0700、文件 0600；Windows 使用当前用户 DPAPI 加密的 apiKeyProtected，不保存明文 apiKey。均使用临时文件原子替换，失败不覆盖既有凭据。Windows 加密文件不能作为跨用户/跨操作系统的可移植密钥。

同一系统用户下的智能体可以共享配置；跨用户/容器通过各自密钥管理器注入。HERMES_HOME 不再影响路径，旧文件不自动读取。

## 命令约定

~~~bash
python scripts/cpris_auth.py login
python scripts/cpris_auth.py login --key-stdin
python scripts/cpris_auth.py login --no-save
python scripts/cpris_auth.py status
python scripts/cpris_auth.py logout
python scripts/cpris_auth.py call GET /childrenInfo/page --query current=1
python scripts/cpris_auth.py call GET /training/list --query date=2026-09-03
python scripts/cpris_auth.py call POST /team/list --body-file request.json
~~~

- login 输入优先级为 --key-stdin、环境密钥、交互终端隐藏输入；无输入的非交互调用报错，不挂起。
- login 先请求 health，再携带 key 请求 /ai/gw/user/user/info。仅在 HTTP 成功、code=200、data 是非空用户对象时保存；失败不覆盖旧凭据。validatedAt 只记录当时验证时间。
- 如果 ACL 不允许 /user/info，不能宣称验证成功。可保留密钥于密钥管理器，直接调用管理员明确开放的业务接口，按实际响应判断。
- status 不请求网络、不显示密钥。logout 删除当前环境文件；环境变量需在宿主清除，服务端撤销由管理员处理。
- --query 支持重复 key=value，格式错误会报错。--body 与 --body-file 二选一，文件使用 UTF-8 JSON（可带 BOM）。
- Python 不存在时，以智能体 HTTP 工具执行等价流程，仍遵守环境隔离、禁止重定向及错误原文不外显的约束。

## 服务端部署对应关系

以下是用户给定域名的部署目标，不是线上探测结果：

| 配置项（前缀 cpris.ai-gateway） | 测试目标 | 正式目标 |
|---|---|---|
| auth.auth-server-url | http://test.cpris.com | https://teacherwx.cpris.com |
| auth.token-path | /ai/key/token | /ai/key/token |
| routes 的业务基地址 | http://test.cpris.com | https://teacherwx.cpris.com |

源码 ai/src/main/resources/application.yml 当前将 auth 和六个路由配置为 http://localhost:3002；部署也可以使用实际内部服务地址。修改技能 aiGateway 不会改变服务端转发目标，环境对应须由部署配置保证。AI 模块监听端口为 3006。

enabled=false 时 health 也返回 503。db-validate=true 时，本地未配置 key 仍交给 auth；api-keys 仅追加 ACL/方法/限流，不替代 t_ai_key。生产与测试部署均需启用 masking.enabled；health 无法证明已开启脱敏。
