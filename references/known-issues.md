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

## 2026-09-09 · Git Bash 会把 -Path /xxx 的前导斜杠转成本地路径

- **现象**：在 Git Bash 中执行 `cpris_call.ps1 -Path /childrenInfo/page`，脚本报 "path contains whitespace, backslash, bad escape or duplicate slash"，实际收到的 Path 已被 MSYS 改写为 `C:/Program Files/Git/childrenInfo/page`。
- **原因**：Git Bash 的 MSYS 路径转换会把以 `/` 开头的参数当作 POSIX 路径映射到安装目录。
- **规避**：命令前加 `MSYS_NO_PATHCONV=1`，或改在 cmd/PowerShell 中直接调用；网关路径必须保持原样以 `/` 开头。

## 2026-09-09 · POST /assessGuide/teacher/guide/list 在 production 返回 500（缺表）

- **现象**：对评估 id 调用教师康复指导列表接口，HTTP 500，后端报 `Table 'c3326.t_assess_define_iep_config' doesn't exist`。
- **原因**：production 数据库缺少 `t_assess_define_iep_config` 表（该量表问卷的 IEP 配置查询直接查库报错），属服务端部署缺陷。
- **规避**：不要重试或换参数；需要"评估→训练条目"关联时改用 `GET /periodical/recent/item/List?childId=...&content=`（返回最近计划明细，含 assessDefineId/subGuideItemId/recoverItem/recoverSubItem），配合 `GET /assess/list`（按 childId+assessProgress=3）定位对应评估实例。

## 2026-09-09 · /periodical/plan/subGuideItem/list 对已落库明细返回空、且评估领域与康复领域码是两套体系

- **现象**：用个训计划明细里的 subGuideItemId（type=1/2/3 各试）调 `POST /periodical/plan/subGuideItem/list` 均返回空数组；`GET /periodical/item/list`（评估推荐 IEP）对 8b01b888 量表返回"无推荐iep数据"。
- **原因**：该勾选转换接口面向"从推荐/IEP 库勾选生成计划"的场景，直接回查已落库明细拿不到映射；推荐 IEP 依赖教师康复指导链路，而该链路查 `t_assess_define_iep_config` 在 production 缺表报 500（见上条），导致推荐数据无法生成。
- **规避**：注意两套领域码不要混用——量表评估领域是 `questionCode`（如 SNAP 类的 tbehavior/tperformance/Cbperformance，来自 /assessDefine/items/list 与 /assess/result/item/info）；计划明细的 `recoverItem`（EMO/ACA/GM/ATT/IMP/SOC）是康复指导领域码，不是量表领域 questionCode。向用户展示"训练条目↔评估领域"时必须用 questionCode 体系，recoverItem 只能作为康复分类参考。

## 2026-09-09 · 【规范】新增个训计划明细的 recoverItem 必须用现有评估的领域代码（questionCode）

- **背景**：迪卡 2026年10月计划明细落库时 `recoverItem` 用了康复领域码（EMO/ACA/GM/ATT/IMP/SOC），与量表评估领域 `questionCode`（如 SNAP 类的 tbehavior/tperformance/Cbperformance）是两套体系，导致训练条目无法正确关联评估领域，已通过 `POST /periodical/plan/saveOrUpdate` 整体改写为 questionCode 修正。
- **规则（今后必须遵守）**：新增/修改个训阶段计划（/periodical/plan/saveOrUpdate）的 planDetailList 时，`recoverItem` 一律填目标评估量表的真实领域代码 questionCode，来源按顺序取：① 该评估 `GET /assess/result/item/info?assessId=` 的 tabResultitemList[].questionCode；② `GET /assessDefine/items/list?assessDefineId=` 的 questionCode。
- **兜底**：用户无法提供/内容无法归入任何现有领域时，`recoverItem` 填 `OTHER`（“其他”量表固定 id `9ac65a3617af4f24b1265b53906e8459`，code=OTHER），保证条目仍能在“其他”评估领域下展示，不允许再使用 EMO/ACA/GM 等康复领域码充当评估领域。
- **保存注意**：saveOrUpdate 是整单覆盖，必须带计划 id 完整回传全部明细（id/recoverSubItem/content/subGuideItemId/assessDefineId/status 原值保留），只改目标字段；写操作失败不自动重试。

## 2026-09-09 · 【他人经验沉淀】个训计划/评估/建档的高频坑（来自其他用户技能包 skills.rar）

> 来源：其他用户的 cpris-training-plan-generator / cpris-child-registration / cpris-assessment-create / cpris-scan-import 四个技能文档，2026-09-09 分析提炼，去重后收录。

### 个训计划（/periodical）
- **`/periodical/year/list` 不按 childId 过滤**：即使传了 childId 也返回（当前教师可见的）全部儿童计划，且返回列表里 planDetailList 可能为空；要拿某儿童计划必须逐条 `GET /periodical/plan/info?planId=` 再核对 childId。
- **saveOrUpdate 成功响应 data 可能为 null**：创建成功不返回计划 id，需事后用 `/periodical/year/list`（按 dgCreatedDate 最新）+ plan/info 找到新计划 id 再核验；更新时必须带计划 id 完整回传。
- **`scheduleDefineId` 可以为 null**：无排课时直接传 null 即可，不必强行查询排课。
- **训练推荐项目层级**：`GET /periodical/item/list` 返回 领域组(item=questionCode/itemName) → teacherSubGuideList → teacherSubGuideItemList（叶子）；planDetail 的 subGuideItemId=叶子 id、content=叶子 content、recoverItem=领域组 item——对 C-PEP-3 这类量表，领域组 item 就是量表 questionCode（P/GM/VMI/FM/EH/CP/CV），与本文件上方 recoverItem 规范一致。推荐项目共 9 个领域（7 核心 + AB 适应行为、PSC 个人自理），训练计划只用 7 个核心领域。
- **弱项分配参考**：按各领域平均发展龄升序（ageRange 字符串 "58~61" split 取均值），项目数按 4/3/3/2/2/1/1 共约 16 条；写入前先查已有计划避免 subGuideItemId 重复。

### 评估（/assess）
- **新建评估的 id 在响应 msg 字段**：`POST /assess/saveOrUpdate` 成功后评估 id 返回在 `msg`（不是 data.data），新建默认 assessProgress="2"（未完成）。
- **/assess/list 的 childName/assessProgress 过滤不可靠**：服务端常忽略过滤参数返回全量，必须客户端按 childId+assessProgress 自行筛选（entityid 是全小写字段名，即评估 id）。
- **重复评估无法通过 API 删除**（删除禁令），需到小程序/后台 UI 处理。

### 建档查重（/childrenInfo）
- **checkName 会漏报**：档案已存在仍可能返回 false，checkName 只能当预检；必须再用 `POST /childrenInfo/list` body {"name":...} 交叉核验（返回空数组=无同名；HTTP 500=IN() 空集合缺陷，同样视为无同名）。
- **不要用 `GET /childrenInfo/page?name=` 做查重/姓名过滤**：无匹配报 SQL IN() 500，且多个 query 参数时可能不按姓名过滤返回全量；姓名过滤一律走 POST /childrenInfo/list body。
- **建档最小请求体**：只传用户点名字段 + childrenVisitList[{jdrq(毫秒时间戳), zdmc(字典诊断text), jdz(接待教师employeeId)}]；jdrq 用毫秒时间戳最稳。写操作警惕沙箱提权重跑导致双写；落库后用 list 唯一性核验（>1 条=重复落库，只能 UI 删）。

### 扫描评估导入（补充 assessment-form-import.md）
- **先判形态再选路径**：有文本层且含 ✓/√ 字形=数字导出版（纯文本解析秒级）；文本层乱/全墨迹=手写扫描版（150DPI 全览+仅对模糊行 400-600DPI 局部放大，不要整页高 DPI）。
- **文字层绝不能当勾选判据**：空圈可能是 O 字形或矢量圈，唯一可靠是渲染后视觉；两个选项同时被勾不擅自挑，列出让用户定。
- **resultContent 骨架可能少于问卷定义总题数**：系统按儿童月龄过滤超龄段题（实测感统 58 题定义只生成 55 题骨架），一律以 result 骨架为准，不硬塞 PDF 上的超龄题。
- **非 C-PEP-3 量表的计分别套 P=1 规则**：中文长选项卷（感统等）objValue 存选项文本、objScore 按问卷定义 tabQuestionScore 分值表映射（如从不这样5…总是如此1）。

### 环境差异（JWT 直连用户补充）
- 旧方案直连业务网关（test.cpris.com / teacherwx.cpris.com）用 JWT Bearer Token，两网关 Token 不通用、JWT 有时效；本技能统一走 AI 网关 X-Api-Key，不适用 Token 问题，但"成功 code=200 不是 0"的判断对所有环境一致。
