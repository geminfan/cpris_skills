# 已知问题与规避（新条目按时间顺序追加到文件末尾）

调用 CPRIS 出现失败、报错或环境异常时，先查本文件是否已有规避方案；新问题解决后把「日期 / 环境 / 现象 / 原因 / 规避」追加到文件末尾，供其他智能体复用，减少重复踩坑和调用耗时。

## 2026-09-07 · 本机无 Python，PowerShell 等价调用

- **现象**：`python scripts/cpris_auth.py ...` 直接退出，exit code 49、无任何输出；`python --version` 同样异常。PATH 中只有 Microsoft Store 的 `python.exe`/`python3.exe` 占位存根（WindowsApps），`py` 启动器不存在。
- **原因**：该 Windows 机器未安装真实 Python。
- **规避**：
  - 用 `scripts/cpris_call.ps1`（本仓库提供的 PowerShell 备用客户端，功能对齐 cpris_auth.py 的常用调用），或按下述模板手工执行等价 HTTP 请求。
  - 长期方案：`winget install Python.Python.3.12` 后可直接用原脚本。
- **已验证可行的 PowerShell 等价流程**：
  1. 凭据解密：读 `%APPDATA%\cpris\cpris-wxapp-rest-api\<env>\credentials.json`，`apiKeyProtected` 为 base64，用 `[System.Security.Cryptography.ProtectedData]::Unprotect(bytes, $null, CurrentUser)` 解出 API-Key（DPAPI 绑定当前用户）。
  2. 请求：`[System.Net.HttpWebRequest]`，`AllowAutoRedirect = $false`、`Accept: application/json`、头 `X-Api-Key`；POST 时 `ContentType: application/json`、正文 UTF-8 字节。
  3. 路由：业务路径按 `references/gateway-config.json` 的 `prefixToService` 映射，如 `/childrenInfo/page` → `<网关>/ai/gw/children/childrenInfo/page`；user 模块为 `/ai/gw/user/...`。

## 2026-09-07 · PowerShell 脚本含中文导致解析错误

- **现象**：UTF-8 无 BOM 的 `.ps1` 内含中文字符串时，报「表达式或语句中包含意外的标记」等解析错误，中文显示成乱码（如 `鐢?`）。
- **原因**：Windows PowerShell 5.1 按 ANSI（GBK）读取无 BOM 的脚本文件。
- **规避**：`.ps1` 保持纯 ASCII（注释用英文）；中文字符串放独立 UTF-8 文件，用 `Get-Content -Encoding UTF8` 读入；向命令行传中文参数同样有编码风险，中文查询值/JSON 正文走文件。

## 2026-09-07 · saveOrUpdate 整体回传实体导致 500 或污染数据

- **现象**：想给儿童改名，先 `GET /childrenInfo/info` 取完整实体，改 name 后原样 `POST /childrenInfo/saveOrUpdate`，返回 HTTP 500 `{"code":500,"msg":null}`。
- **原因**：详情接口返回的是带关联数据的只读拼装结果，不能直接回写：
  - `childrenVisitList` 为 `[null]` 占位（无随访记录时），回传触发服务端空指针；
  - `childrenGuardianList[].phone` 是脱敏值（如 `152****6412`），回写会用掩码覆盖真实手机号；
  - `dgUpdatedBy/dgCreatedDate/etlUpdatedDate` 等审计字段由服务端管理。
- **规避**：字段更新（改名等）只发**最小请求体**：`{"childId":"...","name":"新名字"}`，其余字段为 null 时按非空更新策略不被覆盖。实测返回 `{"msg":"保存成功","code":200}`。
- **附**：500 失败时事务未生效，数据无变化；但不要依赖这一点，写操作前先确认请求体构造正确。

## 2026-09-07 · 儿童列表全量翻页慢

- **现象**：查"我的儿童"共 91 条，默认每页 10 条，需 10 次调用才能取全，输出大（>50KB）还会被截断落盘。
- **规避**：
  - 找特定儿童时用 `GET /childrenInfo/page?name=<姓名>` 过滤，一次命中，不必翻页；
  - 确需全量时按 `total/pages` 字段循环取页，只解析 `data.records[]` 的 `name/sex/birthday/statusName/childId`；
  - 本机密钥已保存在测试环境凭据文件中（见运行时配置），调用前不需要 login/health。

## 2026-09-07 · 新建儿童缺接待日期（jdrq）

- **现象**：儿童"测试ai新建档案2"（2026-09-04 由 geminfan 创建）没有接待日期；`GET /childrenInfo/info` 返回 `"childrenVisitList":[null]`，即无任何接待记录。
- **原因**：接待日期是接待记录表 `t_children_visit` 的 `jdrq` 字段（实体 `TChildrenVisit`，ApiModel 注释"儿童接待记录实体"），按 childId 关联儿童。服务端 `TChildrenInfoServiceImpl.saveOrUpdateAndVisitAndRp` **只在请求体 childrenVisitList 非空时**才插入接待记录；该儿童创建时请求体没带，因此 t_children_visit 无记录、无接待日期。
- **规避（规则）**：新建儿童（`POST /childrenInfo/saveOrUpdate`，无 childId 即新建）必须携带接待日期：
  ```json
  { "name": "...", "sex": "...", "birthday": "...", "childrenVisitList": [ { "jdrq": "<接待日期>" } ] }
  ```
  用户未指定接待日期时默认**当前时间**。`jdrq` 为 java.util.Date，JSON 传 ISO-8601 字符串（如 `2026-09-07T15:30:00`）或毫秒时间戳；visitId/childId/rpId 由服务端生成，无需传。
- **源码确认的 saveOrUpdateAndVisitAndRp 行为**（更新前必读）：
  - 更新已有儿童时传 `childrenVisitList` 会**先删除该儿童全部接待记录再逐条插入**——要传就传完整列表，绝不能传 `[null]` 或残缺数据；`[null]` 在 `visit.setChildId` 处空指针，正是"整体回传实体返回 500"的根因；
  - `childrenGuardianList` 同样先删后插；
  - 新建时服务端固定 `status="2"`（已登记）；
  - 更新走 `updateById`，null 字段不覆盖，所以最小请求体（childId+变更字段）改名安全。

## 2026-09-07 · Git Bash 调 PowerShell 时业务路径被改写

- **现象**：在 Git Bash 中执行 `powershell ... -File cpris_call.ps1 -Method POST -Path /childrenInfo/visit/saveOrUpdate ...`，脚本报"path contains whitespace, backslash, bad escape or duplicate slash"。
- **原因**：MSYS2/Git Bash 会把以 `/` 开头的参数自动转换成 Windows 路径（`/childrenInfo/...` → `C:/Program Files/Git/childrenInfo/...`），传给 powershell.exe 的业务路径被改写。
- **规避**：命令前加 `MSYS_NO_PATHCONV=1`，或用双引号包住并由脚本内部处理；凡从 Git Bash 向 Windows 程序传 `/` 开头参数都要注意。

## 2026-09-07 · 给已有儿童补录接待日期（已验证方案）

- **场景**：儿童已存在但创建时没带接待记录，需补接待日期。
- **已验证**：`POST /childrenInfo/visit/saveOrUpdate`，请求体 `{"childId":"<id>","jdrq":<毫秒时间戳>}`（无 visitId 即插入；jdrq 用毫秒时间戳最稳，避免时区/格式歧义），返回 `{"msg":"保存成功","code":200}`。
- **依据源码**：TChildrenVisitServiceImpl 是纯 MyBatis-Plus saveOrUpdate，visitId 为空走插入（UUID 自动生成、审计字段自动填充）；查询 SQL `getChildrenVisit` 按 `child_id` 过滤、不关联 rpId，补录后 `GET /childrenInfo/info` 能正常查出。走该接口 rpId 为空不影响展示；若业务需要 rpId 关联，改用主接口 `/childrenInfo/saveOrUpdate` 携带完整 childrenVisitList（先删后插）。

## 2026-09-07 · PowerShell 多查询参数不能重复写 -Query

- **现象**：调用 `cpris_call.ps1` 时重复写 `-Query current=1 -Query size=100`，PowerShell 报参数被指定多次；写成 `-Query current=1,size=100` 时，外层 powershell.exe 可能把它绑定成一个字符串，网关收到 `current=1%2Csize%3D100` 并返回数值转换错误。
- **原因**：PowerShell 的数组参数绑定在跨进程 `-File` 调用时容易把逗号表达式当成单个实参；同名参数本身也不能重复出现。
- **规避**：多个查询参数统一写入 UTF-8 `-QueryFile`，每行一个 `key=value`。儿童分页接口每页固定 10 条，`size` 不生效；全量查询直接按响应 `pages` 循环 `current=1..pages`，不要尝试放大页大小。

## 2026-09-07 · 儿童名称筛选空结果会触发 SQL IN () 500

- **现象**：`GET /childrenInfo/page?name=<名称>` 没有匹配儿童时，接口不是返回空 records，而是在补查康复过程时执行 `WHERE child_id IN ()`，产生 MySQL 语法错误并返回 HTTP 500。
- **原因**：儿童分页查询的后续关联查询没有对空 childIds 做短路处理，是当前后端的空集合缺陷。
- **规避**：把该特征性错误视为“名称筛选无匹配”，不要把原始 SQL 错误交付给用户，也不要自动重试同一请求。可用 `/childrenInfo/checkName` 做精确名称存在性校验；若响应数据受脱敏影响、名称查不到或候选不唯一，写操作前必须结合 childId、生日、状态、创建时间等稳定字段让用户确认目标，禁止仅凭脱敏名称猜测写入。

## 2026-09-07 · 已有儿童生日字段的最小更新（已验证）

- **场景**：只修改已有儿童的出生日期，不触碰监护人、接待记录或其他档案字段。
- **已验证**：`POST /childrenInfo/saveOrUpdate`，请求体仅传 `{"childId":"<id>","birthday":"2020-06-17"}`，日期使用 `yyyy-MM-dd`，返回 `{"msg":"保存成功","code":200}`。
- **规避**：先唯一确认 childId，再发送 `childId+birthday` 的最小请求体。不要回传详情实体，不要携带 `childrenVisitList`、`childrenGuardianList`、status 或审计字段；写操作超时或响应不确定时不要自动重试。

## 2026-09-07 · 格赛尔量表需用 Gesell 检索且评估类型为 0

- **现象**：用户常把量表称为“格赛尔评估”；调用 `/assessDefine/list` 用“格赛尔”或“格塞尔”筛选均返回空数组，用英文 `assessDefineName=Gesell` 可以命中。
- **实际定义**：系统量表 code 为“格塞尔发育诊断量表(Gesell)”，`assessDefineType="0"`，属于诊断评估，不是能力评估 `"1"`。
- **规避**：按 `Gesell` 搜索并以接口返回的 `assessDefineId`、`assessDefineType` 为准，不按用户口语名称猜测类型或硬编码量表 id。创建时仍须同时提交 childId、employeeId、assessDefineId、assessType、assessDate、assessAppointDate。

## 2026-09-07 · 正式 AI 网关域名 aiskills.cpris.com 无法解析

- **现象**：对 production 环境调用任何接口均失败，`cpris_call.ps1` 返回 `NO_RESPONSE`（exit 1）；curl 错误码 6（couldn't resolve host）。
- **原因**：`aiskills.cpris.com` 在本机 DNS（OrayBox）及公共 DNS（223.5.5.5、8.8.8.8）均为 NXDOMAIN，域名无解析记录；同 IP 段的 `teacherwx.cpris.com`、`testai.cpris.com` 均正常解析。属服务端 DNS/部署未就绪，非客户端问题。
- **规避**：遇到 `NO_RESPONSE`/curl 6 先 `nslookup` 区分 DNS 与网络问题；正式网关域名解析恢复前无法访问 production。注意：production 密钥在 testai 网关返回 401，密钥环境不通用，不要拿 production 密钥打 test 网关排查。

## 2026-09-08 · 生成 IEP 康复指导：直调 generate 500，改查空自动生成（已验证）

- **现象**：`POST /assessGuide/generate`，body `{"assessId":"..."}` 直接生成 IEP，返回 HTTP 500（`{"code":500,...}`），且不产生任何数据。
- **规避（已验证）**：改用 `POST /assessGuide/teacher/guide/list`，body `{"assessId":"..."}`——教师 IEP 列表为空时服务端会自动生成并落库，再次查询即返回已生成的 IEP；教师端模块用 `teacher`，家长端为 `parent`。
- **后续建个训计划的推荐数据来源**：`GET /periodical/item/list?assessDefineId=<defineId>&childId=<childId>`，返回多个领域的 `teacherSubGuideList` → `teacherSubGuideItemList[].id`（即推荐子项 id），可据此构造个训计划明细。

## 2026-09-08 · 结果/生成接口的领域名被网关遮盖，全名从问卷定义对照

- **现象**：`/assess/result/list`、`/assess/result/generate` 返回的 `tabResultitemList[].questionCodeName` 被网关按展示权限遮盖，如「模*」「知*」，不能直接把该值交付给用户。
- **规避**：全名不受遮盖，须从问卷定义取：`GET /assessDefine/paper/list?assessDefineId=<defineId>` → `paperContent`(JSON 字符串) → `tabResultitemList[]`，用 `questionResultId` ↔ `questionCodeName` 一一对应做键对照出领域全名；**数值仍以 result 类接口返回值为准**，不要用问卷定义中的静态默认值推算。

## 2026-09-08 · 个训阶段计划创建与校验（已验证流程）

- **建计划链路**：
  1. 推荐子项 id 列表转明细：`POST /periodical/plan/subGuideItem/list`，body 为数组，每领域一项 `{"type":"1","assessDefineId":"<defineId>","subGuideItemIds":[...]}`，返回含 `item/subItem/content/id` 的明细对象；
  2. 创建：`POST /periodical/plan/saveOrUpdate`，body `{"childId":...,"childName":...,"name":...,"fromDate":...,"toDate":...,"planDetailList":[...]}`。`teacherName` 服务端强制为当前用户；`status=1`(草稿)、`type=01`(个训)、康复档案 rpId 自动关联，无需也不应传。
- **坑**：`GET /periodical/year/list?date=<年>` 返回记录的 `planDetailList` 恒为空数组（列表接口不含明细），**不能据此确认明细条数**；校验明细须用 `GET /periodical/plan/info?planId=<id>`。

## 2026-09-08 · cpris_auth.py call 输出重定向到文件偶发失败

- **现象**：`python scripts/cpris_auth.py call GET ... > out.json` 偶发报「配置、输入或文件操作失败」，落盘内容为空或失败；不重定向直接看 stdout 正常。
- **规避**：疑似瞬时文件句柄/缓冲问题，重定向失败时**换一个文件名重试即成功**；大 JSON 解析前用唯一文件名（如 `tmp_*.json`）重定向，失败就换名重试，或先不加 `>file` 直接查 stdout。
