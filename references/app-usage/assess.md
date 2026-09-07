# 评估模块（/assess*）实际调用接口

Controller：`AssessController`（/assess）、`AssessDefineController`（/assessDefine）、`AssessGuideController`（/assessGuide）、`CarsController`（/assess/cars）、`Mte1Controller`（/assess/mte1）。AI 网关 service=assess。

## 一、评估记录（/assess）

### GET /assess/page — 评估分页
- 前端：`childApi.assessPage`（evaluate/itemScale.vue 列表/搜索）
- AI 网关：✅ 可调用

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| current | query | long | 否（默认1） | 页码，每页固定 10 条 |
| childName | query | string | 否 | 儿童姓名模糊匹配 |
| userId | query | string | 否 | 评估教师 employeeId 精确匹配 |
| assessProgress | query | string | 否 | 1未评估 / 2未完成 / 3已完成 |

- 响应 `data`：Page；records 元素含 `entityid`（评估id）、`assessProgress`、`assessDefineName`、`childId`、`childName`、`userName`（教师名）等 VSmdAssess 字段。
- 后端限制：按创建时间倒序（dg_created_date DESC，不是预约时间）；每条回填评估定义名称与教师/家长指导标识。

### POST /assess/saveOrUpdate — 新建/修改评估
- 前端：`childApi.assessSaveOrUpdate`（evaluationContent.vue 新建与编辑）
- AI 网关：✅ 可调用

请求体 VSmdAssess（前端实际传）：

| 字段 | 类型 | 必填 | 前端来源 / 后端说明 |
|---|---|---|---|
| entityid | string | 更新必填 | **键名全小写 entityid**；无值=新建（服务端生成 UUID），有值=修改 |
| childId | string | 是 | 儿童 id（新建时写入） |
| employeeId | string | 是 | 评估教师 employeeId |
| assessDefineId | string | 是 | 评估定义（量表）id |
| assessType | string | 是 | 评估类型（TAssessDefine.assessDefineType，能力评估为 "1"） |
| assessDate | string/时间戳 | 是 | 实际评估时间，@JsonFormat yyyy-MM-dd HH:mm:ss（前端传 yyyy-MM-dd HH:mm） |
| assessAppointDate | string/时间戳 | 可选 | 预约时间；**新建和修改都被后端强制置为 =assessDate**，传不同值无效 |
| realAssessPerson | string | — | **此接口不写入该字段**（更新为显式 set 白名单）；实际评估人由 /assess/finish、/assess/result/generate、/assess/report/generate 自动写当前用户 |

- 响应：`{"code":200,"msg":<entityId>}` — **msg 是评估 id**，前端用它跳转。
- 后端约束：body 空对象→400"请求参数错误"；新建时插 TSmdAssess 基表（entityType="assess"）并写 assessProgress="2"；**写入字段为显式白名单**——新建：assessDate、assessAppointDate(=assessDate)、assessProgress、childId、employeeId、assessDefineId、assessType；修改：同前去掉 childId（**不能经此接口改评估所属儿童**），其余字段（含 realAssessPerson）一律不落库。
- 不要用 dgCreatedDate/dgCreatedBy 等审计字段代替评估时间/评估老师。

### GET /assess/info — 评估详情
- 前端：`childApi.assessInfo`（answeringItem.vue）
- AI 网关：✅ 可调用

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| assessId | query | string | **是** | 评估 id（=entityid） |

- 响应 `data`：VSmdAssess（含 childName、userName 联查回填）。

### POST /assess/result/saveOrUpdate — 保存问卷答案（标准量表）
- 前端：`childApi.assessResultSaveOrUpdate`（answeringPage.vue saveDraft）
- AI 网关：✅ 可调用

请求体 TAssessResultValue：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| entityId | string | 是 | 评估 id（**键名 entityId，与 /assess/saveOrUpdate 的 entityid 不同**） |
| assessDefinePaperId | string | 是 | 问卷 id |
| paperType | string | 是 | "0" 教师卷 / "1" 家长卷（前端固定 "0"） |
| resultContent | string(JSON) | 是 | 问卷答案 JSON 字符串，结构见下 |
| resultId | string | 更新必填 | 结果 id；空=插入（服务端生成 ASSIGN_UUID），非空=按主键更新 |

resultContent 结构（`JSON.stringify`）：普通量表 `{"tabAttrList":[...], "tabQuestionList":[{questionCodeName, questionId, rowSort, questionCode, questionType, questionDetail, assessValueList:[{objValue, objScore}]}]}`；C-PEP-3 的 tabAttrList 元素为 `{attrId, attrName, attrType, assessValueList:[{objValue}]}`。
- 响应：`{"code":200,"msg":"保存或修改成功"}`。
- 后端约束：标准 MP saveOrUpdate，无内容校验；答案完整性由 /assess/result/status/map 判定。更新已有记录必须保留 resultId/entityId/assessDefinePaperId/paperType。完整答案超过命令行长度时用 --body-file（见 assessment-form-import.md）。

### GET /assess/result/list — 评估全部问卷结果
- 前端：`childApi.assessResultList`（answeringTabAttrList.vue 回显）
- AI 网关：✅ 可调用

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| assessId | query | string | **是** | 评估 id |

- 响应 `data`：TAssessResultValue 数组（该评估所有问卷结果，含 resultContent/resultitemContent JSON、assessDefinePaperId）。

### GET /assess/result/info — 单问卷结果
- 前端：`childApi.assessResultInfo`（answeringPage.vue 回显已答）
- AI 网关：✅ 可调用

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| assessId | query | string | **是** | 评估 id |
| assessDefinePaperId | query | string | **是** | 问卷 id |

- 响应 `data`：TAssessResultValue；前端解析 `resultContent` 的 `tabAttrList[].assessValueList[0].objValue`、`tabQuestionList[].questionId/assessValueList[0].objValue` 回显。

### POST /assess/result/generate — 生成评估结果（写操作）
- 前端：`childApi.assessResultGenerate`（6 处：提交前/编辑后/新增后/生成报告）
- AI 网关：✅ 可调用

请求体 AssessVo：`{"assessId":"..."}`（仅此一个字段）。
- 响应 `data`：AssessResultValueItemContent（领域结果，见 /assess/result/item/info）；无结果时 data 为字符串 "该评估暂无领域结果"。
- 后端约束：评估不存在→"评估不存在"；内部 Playwright 渲染报告 PDF 并上传；**同时把评估置为已完成**（assessProgress="3"、realAssessPerson=当前用户）。重操作，不自动重试；超时不代表失败。

### GET /assess/result/item/info — 领域结果查询
- 前端：`childApi.assessResultItemInfo`（evaluationResults.vue）
- AI 网关：✅ 可调用

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| assessId | query | string | **是** | 评估 id |

- 响应 `data`：AssessResultValueItemContent：`assessEntityid`、`ageRange`、`developmentScore`、`tabResultitemList[]`（元素 `questionCodeName`、`questionCode`、`assessValueList[0].objValue`）。无结果→"暂无数据"。

### POST /assess/result/item/saveOrUpdate — 保存领域结果（PEP-3 触发指导重算）
- 前端：`childApi.assessResultItemSaveOrUpdate`（evaluationResults.vue submitReport）
- AI 网关：✅ 可调用

请求体 AssessResultValueItemContent：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| assessEntityid | string | 是 | 评估 id（**键名 assessEntityid**） |
| ageRange | string | 是 | 年龄区间（来自 item/info 回显） |
| developmentScore | string | 是 | 发展分 |
| tabResultitemList | TabResultitem[] | 是 | 领域明细；元素 `{questionCode, questionCodeName, assessValueList:[{objValue}]}` |

- 响应：`{"code":200,"msg":"保存成功"}`。
- 后端约束：评估定义 code 为 "PEP-3（香港版本）" 时，questionCode 必须 ∈ {AB, CVP, EL, RL, FM, GM, VMI, PSC}，CVP/EL/RL/FM/GM/VMI 须可转 Long、PSC 转 Integer（错值抛 NumberFormatException）；会先删后重建教师/家长 IEP（Redis 锁），并将整个对象序列化回写该评估**所有** TAssessResultValue.resultitemContent，再重渲染 PDF。

### GET /assess/result/status/map — 问卷完成状态
- 前端：`childApi.assessResultStatusMap`（answeringItem.vue，非中评非 CARS 量表）
- AI 网关：✅ 可调用

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| assessId | query | string | **是** | 评估 id |

- 响应 `data`：Map（key=assessDefinePaperId，value="1" 完成 / "0" 未完成）。
- 判定规则：解析问卷必答题（TabQuestion.isRequired），必答题无 assessValueList、objValue 为空或等于哨兵值 `"xxxxx"` → 未完成。

### GET /assess/report/info — 报告文件信息
- 前端：`childApi.assessReportInfo`（4 处 viewReport）
- AI 网关：✅ 可调用

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| assessId | query | string | **是** | 评估 id |

- 响应 `data`：`{date, path}`；path 为报告文件路径 + "/{ticket}"（票据 5 分钟有效），拼文件下载地址用。
- 后端约束：本地已有 PDF 直接返回；无文件且评估已完成（"3"）则现场 Playwright 渲染生成；未完成→"评估未完成，请先完成评估"。

### POST /assess/report/summary/generate — 导入简述模板
- 前端：`childApi.assessReportSummaryGenerate`（reportSummary.vue）
- AI 网关：✅ 可调用。请求体 `{"assessId":"..."}`。
- 响应：**`msg`/`data` 为模板 HTML 文本**（前端取 result.msg 填入编辑框）。报告 URL 为空→"生成失败，评估不存在"。

### GET /assess/report/summary/info — 取报告简述
- 前端：`childApi.assessReportSummaryInfo`（reportSummary.vue）
- AI 网关：✅ 可调用。query：assessId（必填）。
- 响应：`msg` 为第一条结果的 summary 文本；无结果→"报告不存在"。

### POST /assess/report/summary/update — 修改报告简述
- 前端：`childApi.assessReportSummaryUpdate`（reportSummary.vue 提交）
- AI 网关：✅ 可调用

请求体 AssessVo：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| assessId | string | 是 | 评估 id |
| reportSummary | string | 是 | 简述文本（前端为多行文本） |

- 响应：`{"code":200,"msg":"修改成功"}`。后端把 summary 写入该评估**所有**问卷结果并重渲染 PDF。

### POST /assess/delete — 删除评估
- 前端：`childApi.assessDelete`（evaluate/itemScale.vue）。请求体 `{"assessId":"..."}`。
- AI 网关：❌ 禁止（删除禁令）。后端删除全部结果值、评估本体与报告目录。

## 二、评估定义（/assessDefine）

### GET /assessDefine/list — 量表列表（机构可用）
- 前端：`childApi.assessDefineList`（institutionIEP.vue、addTrainingContent.vue）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| type | query | string | 否 | 评估定义类型码（见枚举） |
| assessDefineName | query | string | 否 | 名称模糊 |

- 响应 `data`：TAssessDefine 数组（assessDefineId、assessDefineName、assessDefineCode…）。
- 后端限制：固定过滤 已发布（status="0"）+ 机构套餐内 + **排除 freeFlag="1"**；按 sort 升序。AI 网关 ✅。

### GET /assessDefine/andOther/list — 量表列表（追加"其他"）
- 前端：`childApi.assessDefineAndOtherList`（myIEP.vue 传 type、addMyIEP.vue 传 {}）
- 同 /assessDefine/list，末尾固定追加：assessDefineId=`9ac65a3617af4f24b1265b53906e8459`、code="OTHER"、名称"其他"。AI 网关 ✅。

### GET /assessDefine/page — 量表分页
- 前端：`childApi.assessDefinePage`（evaluate/itemRecord.vue）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| current | query | long | 否（默认1） | 每页固定 10 条 |
| type | query | string | 否 | 类型码 |
| assessDefineName | query | string | 否 | 前端参数名为 assessDefineName（搜索词） |

- 响应 `data`：Page（TAssessDefine）。过滤条件同 list。AI 网关 ✅。

### GET /assessDefine/type/count — 各类型量表数量
- 前端：`childApi.assessDefineTypeCount`（2 处）。无参数。
- 响应 `data`：`[{type, count}]`。AI 网关 ✅。

### GET /assessDefine/type/map — 类型码表
- 前端：`childApi.assessDefineTypeMap`（evaluate/itemRecord.vue，固定传 freeFlag=0&status=0&type=1&version=1，后端**均忽略**）
- 响应 `data`：Map（类型码→`{name, text}`）。缓存来源 `assess.getAssessType`。AI 网关 ✅。

### GET /assessDefine/items/list — 领域 item 列表
- 前端：`childApi.assessDefineItemsList`（teacherGuidance.vue、addMyIEP.vue）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| assessDefineId | query | string | **是** | 量表 id（"其他"固定 id 也可） |

- 响应 `data`：TabResultItem 数组（questionCode、questionCodeName、sort；content/mapper 明细被清空）。AI 网关 ✅。

### GET /assessDefine/paper/list — 问卷定义列表
- 前端：`childApi.assessDefinePaperList`（answeringItem/answeringPage/answeringTabAttrList）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| assessDefineId | query | string | **是** | 量表 id |

- 响应 `data`：TAssessDefinePaper 数组：`assessDefinePaperId`、`paperType`（0教师/1家长）、`sort`、`paperContent`（**JSON 字符串**，含 tabAttrList/tabQuestionList/tabExplainList/tabResultitemList/labelName）。AI 网关 ✅。不要硬编码问卷 ID 或题目数量，以本接口返回为准。

## 三、康复指导 IEP（/assessGuide）

### POST /assessGuide/teacher/guide/list — 教师 IEP 列表
### POST /assessGuide/parent/guide/list — 家长 IEP 列表
- 前端：`childApi.assessGuideTeacherGuideList` / `assessGuideParentGuideList`（teacherGuidance.vue、parentGuidance.vue）
- 请求体均为 `{"assessId":"..."}`。AI 网关 ✅。
- 响应 `data`：按评估定义 code 返回对应指导列表（普通/SAM），元素含回填 itemName。
- 后端约束：**查询为空时会在锁内自动生成并保存** IEP（有写副作用）；生成前提是该评估已有问卷结果且领域分可解析，否则报"评估未完成，请先完成评估"。

## 四、CARS 量表（/assess/cars）

### GET /assess/cars/question/list — CARS 题目与回显
- 前端：`childApi.assessCarsQuestionList`（answeringPage.vue，量表名="CARS儿童孤独症评定量表"）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| assessId | query | string | **是** | 评估 id |

- 响应 `data`：`{itemMap, typeMap, resultListMaps}`：typeMap 逐 key 生成题目（元素含 id、LEVEL、ONE、TWO 分值选项），itemMap[key] 为题目数据，resultListMaps 已答记录（score/item/qid/type）。AI 网关 ✅。

### POST /assess/cars/result/saveOrUpdate — 保存 CARS 答案
- 前端：`childApi.assessCarsResultSaveOrUpdate`（answeringPage.vue 提交）

请求体 CarsResultVo：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| carsResultList | TAssessCarsPaper[] | 是 | 元素 `{assessId, item:题目LEVEL, qid, score:所选分值, type:题目id}`；qid 服务端会重写为 UUID |

- 响应：`{"code":200,"msg":"保存成功"}`。
- 后端约束：列表空→"请求参数错误"；以第一条的 assessId 查评估，不存在→"评估不存在"；答案**先删后插**；同时组装/更新领域结果 resultitemContent 并渲染报告 PDF。AI 网关 ✅。

### GET /assess/cars/result/status/map — CARS 完成状态
- 前端：`childApi.assessCarsResultStatusMap`（answeringItem.vue）。query：assessId（必填）。
- 响应 `data`：Map；已答题目记录数 **≥15** 才返回 `{"<assessDefinePaperId>":"1"}`，否则空 map。AI 网关 ✅。

## 五、中评 MTE-1（/assess/mte1）

### GET /assess/mte1/teacher/question/list — 教师卷题目
- 前端：`childApi.assessMte1TeacherQuestionList`（answeringPage.vue，userType=="teacher"）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| assessId | query | string | **是** | 评估 id |

- 响应 `data`：`{questionsMap, qMap(改善情况+cljy), analysisMap(适应性), dealMap(反思), result(主结果，含 psuggestion), resultListMaps}`。评估不存在→"评估不存在"。AI 网关 ✅。

### GET /assess/mte1/parent/question/list — 家长卷题目
- 前端：`childApi.assessMte1ParentQuestionList`（answeringPage.vue，userType=="parent"）。query：assessId（必填）。
- 响应 `data`：同上但 analysisMap/dealMap 为空（后端取的也是 paperType="0" 题目，仅保留改善情况桶）。AI 网关 ✅。

### POST /assess/mte1/result/saveOrUpdate — 保存中评结果
- 前端：`childApi.assessMte1ResultSaveOrUpdate`（answeringPage.vue saveDraft2）

请求体 Mte1ResultVo：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| assessId | string | 是 | 评估 id |
| parentPaperList | [{id,qid,qvalue,resultId}] | 家长登录时 | qvalue 为选项分值 |
| teacherResultList | [{analysisValue,dealValue,id,qid,qvalue,resultId}] | 教师登录时 | 同上 |
| cljyResult | TAssessMte1Result | 是 | 处理建议对象（含 id、psuggestion、psuggestionSelect）；id 空=新建 |

- 响应：`{"code":200,"msg":"保存成功"}`。
- 后端约束：教师卷/家长卷**先删后插**（按 resultId）；计分规则：qid≠5 时答案 1→2分、2/3→1分、4→0分，qid=5 时 1→2分、2→1分、3→0分；总分 >7 显效、>1 有效、≤1 无效，自动写入 teacherAssessResult/parentAssessResult。AI 网关 ✅。

### GET /assess/mte1/result/status/map — 中评完成状态
- 前端：`childApi.assessMte1ResultStatusMap`（answeringItem.vue）。query：assessId（必填）。
- 响应 `data`：Map；教师卷 ≥5 条→"1"，家长卷 ≥5 条→"1"，默认 "0"。AI 网关 ✅。

## 前端未调用、后端存在的接口

| 接口 | 请求 | 说明 | AI |
|---|---|---|---|
| GET /assess/list | query childName/userId/assessProgress（均可选） | 不分页版评估列表，过滤同 /assess/page | ✅ |
| POST /assess/finish | query assessId（必填） | 标记完成：assessProgress="3"、realAssessPerson=当前用户 | ✅ |
| POST /assess/unFinish | query assessId（必填） | 标记未完成：assessProgress="2" | ✅ |
| POST /assess/report/generate | `{"assessId":"..."}` | 仅生成报告 PDF（不做结果计算），前端已弃用改用 /assess/result/generate | ✅ |
| POST /assess/result/delete | 无参 | 清理孤儿结果数据（hidden 接口） | ❌ 删除禁令 |
| POST /assessGuide/generate | `{"assessId":"..."}` | 双锁内并行生成教师+家长 IEP（异步、join 等待）；通常无需显式调，guide/list 查空自动生成 | ✅ |

## 关键实体

### VSmdAssess（评估视图实体，/assess/saveOrUpdate 请求体与各查询返回）
常用字段：`entityid`（评估主键）、`childId`、`employeeId`、`assessDefineId`、`assessType`、`assessDate`、`assessAppointDate`（@JsonFormat yyyy-MM-dd HH:mm:ss）、`assessProgress`（1/2/3）、`realAssessPerson`、`diagnosis`、`tentativeDiagnosis`、`withParents`、`assessedHour/assessedMinutes`、`advantage/disadvantage`、查询回填 `assessDefineName/childName/userName/teacherGuideFlag/parentGuideFlag`；审计字段 dg*/etl* 服务端管理。

### TAssessResultValue（问卷结果）
`resultId`（ASSIGN_UUID）、`entityId`（评估id）、`assessDefinePaperId`、`paperType`（0/1）、`resultContent`（问卷答案 JSON 字符串）、`resultitemContent`（领域结果 JSON 字符串）。

### AssessResultValueItemContent（领域结果）
`assessEntityid`、`ageRange`、`developmentScore`、`summary`、`tabResultitemList[]`：`{questionCode, questionCodeName, labelName, ageRange, developmentScore, assessValueList:[{objKey, topicType, objValue, auditValue}]}`。

### TAssessDefine（评估定义）
`assessDefineId`、`assessDefineName`、`assessDefineCode`（如 C-PEP-3、PEP-3（香港版本）、高功能社会性评估）、`assessDefineType`（类型码）、`assessDefineStatus`（0已发布/1未发布/2停用）、`questionNaire`（0教师/1家长/2双卷）、`version`、`assessDefineCycle` 复评周期、`freeFlag`、`ageRange`(月)、`teacherGuideFlag/parentGuideFlag`、`teacherPaperFlag/parentPaperFlag`、`assessDefineSort`。

### TAssessDefinePaper（问卷）
`assessDefinePaperId`、`assessDefineId`、`paperType`、`sort`、`paperContent`（Tab 结构 JSON 字符串）。

## 枚举与常量

- assessProgress：`1` 未评估、`2` 未完成（新建默认）、`3` 已完成。
- paperType：`0` 教师卷、`1` 家长卷。
- 评估定义类型 assessDefineType（=评估记录 assessType）：`0` 诊断评估、`1` 能力评估、`2` 疗效检测、`4` 筛查评估、`5` 行为评估、`6` 其他、`7` 感知觉量表。
- PEP-3（香港版）领域码 questionCode：`AB` 适应行为等级（文本，"严重"归一为"重度"）、`CVP` 认知、`EL` 表达语言、`RL` 接受语言、`FM` 精细动作、`GM` 粗大动作、`VMI` 视觉动作模仿（数值分）、`PSC` 口部肌肉运动年龄。
- "其他"量表固定 id：`9ac65a3617af4f24b1265b53906e8459`（code=OTHER，items 返回 questionCode=OTHER/"全部"）。
- 完成判定：普通量表按必答题逐题检查（objValue 空/`"xxxxx"` 即未完成）；CARS ≥15 题；MTE-1 教师/家长卷各 ≥5 题。
- MTE-1 结论：总分>7 显效、>1 有效、≤1 无效。
- 报告 URL 按 assessDefineCode 路由（CARS→/assess/cars/report/{id}、中评→/assess/mte1/report/{id}、C-PEP-3→/assess/report/generatecpep3/{id} 等），服务端内部使用；报告票据 5 分钟有效。
- Redis 锁：`assess:teacher:{assessId}` / `assess:parent:{assessId}`（IEP 生成互斥）。
