# 训练模块（/team、/periodical、/training、/iepLib）实际调用接口

Controller：`TeamController`（/team）、`PeriodicalController`（/periodical）、`TrainingController`（/training）、`IepLibController`（/iepLib）。AI 网关 service=training，如 `/ai/gw/training/team/list`。查询类接口按当前用户（token）过滤的居多。

## 一、小组课（/team）

### POST /team/list — 小组列表
- 前端：`childApi.teamList`（subpackageA/chooseChildren.vue 选组）
- AI 网关：✅ 可调用

请求体 GroupVo（均可选）：

| 字段 | 类型 | 说明 |
|---|---|---|
| name | string | 小组名称模糊匹配 |
| leader | string | 组长/副组长 employeeId 精确 |
| suitLevelList | string[] | 适用等级（lowfunction/middlefunction/hignfunction） |

前端固定传 `{"leader":"", "name":"<搜索词>", "status":1, "suitLevelList":["lowfunction","middlefunction","hignfunction"]}`（status 后端忽略，SQL 固定 status='1'）。
- 响应 `data`：TGroup 数组（`groupId`、`name`、`leaderName`、`memberNum` 在组人数等）。

### GET /team/count — 有效小组数
- 前端：`childApi.teamCount`（course.vue）。无参数。响应 `data`：int（status='1'）。AI ✅。

### GET /team/child/enter/list — 在组儿童
- 前端：`childApi.teamChildEnterList`（courseRecord.vue）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| groupId | query | string | **是** | 小组 id（含子小组 `groupId.%` 前缀） |

- 响应 `data`：TRecoverProcessGroup 数组（`childId`、`childName`、`rpId`…），固定 status="2" 在组。AI ✅。

### GET /team/lesson/info — 组课详情
- 前端：`childApi.teamLessonInfo`（groupLesson.vue 编辑回显、courseRecord.vue）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| scheduleDefineId | query | string | **是** | 排课定义 id |

- 响应 `data`：TStratoScheduleDefine：`scheduleDefineId`、`repeatType`、`startDate/overDate`、`timeRange`（"HH:mm~HH:mm"）、`teamv3ParticipantList[0].participantId/participantName`（小组）、`teamv3SchemeStepList[]`（`employeeId/employeeName/teacherType(1主训/2辅训)/schemeStepId(逗号串)/scheduleExtendId`）、`schemeIdList`。AI ✅。

### POST /team/lesson/saveOrUpdate — 新建/修改组课
- 前端：`childApi.teamLessonSaveOrUpdate`（groupLesson.vue submit）
- AI 网关：✅ 可调用

请求体 TStratoScheduleDefine（前端实际传）：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| scheduleDefineId | string | 更新必填 | 空=新增（服务端生成 UUID；endDate 强制=startDate） |
| startDate | string/时间戳 | 是 | 开始日期 |
| overDate | string/时间戳 | 否 | 截止日期；repeatType="0" 前端置 "" |
| timeRange | string | 是 | "HH:mm~HH:mm"（startTime+"~"+endTime） |
| repeatType | string | 是 | 0不重复/1每日/2每周/3每月/4隔天/5工作日 |
| teamv3ParticipantList | [{participantId, participantType:"1", scheduleExtendId}] | 是 | 参与小组；participantType 后端强制 "1"（儿童组） |
| teamv3SchemeStepList | [{employeeId, scheduleExtendId, schemeStepIds:[...], teacherType}] | 是 | 主训/辅训两项；teacherType 1主训 2辅训；schemeStepIds 为教案步骤 entityid 数组 |

- 响应：`{"code":200,"msg":"保存成功"}`。
- 后端约束（@Transactional）：修改时先物理删原 participant/schemeStep/assign 再重插（全量替换）；空 body→"请求参数错误"。**修改时必须回传完整参与人与步骤列表**。

### POST /team/lesson/onlyOne/delete — 删除某天单次组课
- 前端：`childApi.teamLessonOnlyOneDelete`（3 处）。请求体 `{"scheduleDefineId":"...", "date":"yyyy-MM-dd"}`（前端格式化可能为 yyyy-M-d）。
- AI 网关：❌ 禁止（删除禁令）。
- 后端行为：先删该 define 全部 instance/instanceAssign，再按 repeatType 拆分前段/后段；日期 ≥ overDate 时整条删除。

### POST /team/lesson/delete — 删除整个组课
- 前端：定义未调用。请求体 `{"scheduleDefineId":"..."}`。AI ❌ 禁止。物理删除 6 类关联数据（含全部总结）。

### GET /team/lesson/summary/type/list — 总结评分维度
- 前端：`childApi.teamLessonSummaryTypeList`（courseRecord.vue）。无参数。
- 响应 `data`：SysBasedata 数组；`extra1` 为逗号分隔的星级文案（如 "好,较好,一般,差"），`extra2` 为评分落库字段序号（0→score0 学习情况，1→score1 行为情绪）。AI ✅。

### GET /team/lesson/summary/info — 组训总结回显
- 前端：`childApi.teamLessonSummaryInfo`（courseRecord.vue）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| scheduleDefineId | query | string | **是** | 排课定义 id |
| workDate | query | string | **是** | yyyy-MM-dd（hutool 严格按此格式解析） |

- 响应 `data`：`{schInsId, status, remarks, teamLessonV2RpList[]（含 childId、score0/score1…、present）}`。AI ✅。

### POST /team/lesson/summary/saveOrUpdate — 保存组训总结
- 前端：`childApi.teamLessonSummarySaveOrUpdate`（courseRecord.vue submit）
- AI 网关：✅ 可调用

请求体 TeamLessonSummaryVo：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| scheduleDefineId | string | 是 | 排课定义 id |
| workDate | string/时间戳 | 是 | 上课日期 |
| status | string | 否 | 总结状态 |
| remarks | string | 否 | 课程总结文本 |
| schInsId | string | 编辑必带 | 总结实例 id（回显值；空=新建） |
| teamLessonV2RpList | TTeamLessonV2Rp[] | 是 | 每儿童一条：`{lessonId(=scheduleDefineId), childId, present(0请假/1到场/2缺席), workDate}` + 按 summary/type/list 的 extra2 动态生成的评分键（`score0`/`score1`…，值为星级数或 ""） |

- 响应：`{"code":200,"msg":"保存成功"}`。
- 后端约束：teamLessonV2RpList 非空时**先按 lessonId 物理删旧总结再插入**（全量替换）；schInsId 空=新建 TStratoScheduleInstance（status="0" 完成）+assign（执行人=当前用户）。

### GET /team/dateRange/page — 日期区间组课分页
- 前端：`childApi.teamDateRangePage`（course/itemScale.vue）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| current | query | long | 否（默认1） | 每页固定 10 条 |
| startDate / endDate | query | string | 否 | yyyy-MM-dd；均空/只传其一时自动补全为该周周一~周日 |
| groupId | query | string | 否 | 小组 id |
| childName | query | string | 否 | 儿童姓名模糊（会带出其所在小组的课） |

- 响应 `data`：Page（TStratoScheduleDefine，含步骤/参与人/summaryStatus）。排序：日期降序、timeRange 升序。查询按当前用户（主/辅训老师）过滤。AI ✅。

### GET /team/scheme/type/list — 教案类型
- 前端：`childApi.teamSchemeTypeList`（institutionalTeachingPlan.vue tab）。无参数。
- 响应 `data`：SysBasedata 数组（`text`/`value`，字典 teamCourceSchemeType）。AI ✅。

### POST /team/scheme/page — 机构教案库分页
- 前端：`childApi.teamSchemePage`（institutionalTeachingPlan.vue）
- AI 网关：✅ 可调用。**注意 `current` 是 query 参数**，其余过滤在 body。

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| current | query | long | 否（默认1） | 每页固定 10 条 |
| (body) SchemeVo | JSON | — | 见下 |

SchemeVo：`name` 模糊、`type` 精确（tab 类型值）、`author/groupId/status` 精确、`target/extension/parentGuide` 模糊、`levelList` **后端未使用**。前端固定传空串占位。
- 响应 `data`：Page（VSmdCourseScheme：`entityid`（教案主键）、`courseSchemeName`、`schemeStepList[0].entityid`、类型/等级名等）。

### GET /team/scheme/info — 教案详情
- 前端：`childApi.teamSchemeInfo`（teachingPlanDetail.vue）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| schemeId | query | string | **是** | 教案 entityid（兜底 courseSchemeId） |

- 响应 `data`：VSmdCourseScheme 含 `schemeStepList[]`（stepDisplayOrder/stepContent）、`schemeToolList[]`（toolDisplayOrder/toolContent）、`schemeFileList[]`。不存在→"暂无该教案"。AI ✅。

### POST /team/scheme/step/list — 教案步骤批量查询
- 前端：`childApi.teamSchemeStepList`（groupLesson.vue）
- 请求体：**字符串数组**（教案步骤 entityid 列表，如 `["id1","id2"]`）。空数组返回空列表。
- 响应 `data`：VSmdCourseScheme 数组（每条含对应 schemeStepList，step 附 schemeName）。AI ✅。

## 二、个训计划（/periodical）

### GET /periodical/item/list — 推荐 IEP 项目
- 前端：`childApi.periodicalItemsList`（addTrainingContent.vue tab"推荐项目"）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| assessDefineId | query | string | **是** | 量表 id |
| childId | query | string | **是** | 儿童 id |
| content | query | string | 否 | 前端传搜索词（后端忽略） |

- 响应 `data`：推荐 IEP 列表（元素含 id、teacherSubGuideList[].teacherSubGuideItemList[].id）；无已完成评估或量表不属 C-PEP-3/PEP3/SAM 时 data 为字符串 "无推荐iep数据"。
- 后端约束：取该儿童该量表**最近一次已完成**（assessProgress="3"）评估生成。AI ✅。

### GET /periodical/recent/item/List — 近期干预 IEP
- 前端：`childApi.periodicalRecentItemList`（recentInterventionIEP.vue、addTrainingContent.vue）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| childId | query | string | **是** | 儿童 id |
| content | query | string | **是**（required 默认 true） | 康复指导文本模糊过滤；**null 会拼成 LIKE '%null%'，传空串""** |
| assessDefineId | query | string | 否 | 前端部分页面传 |

- 响应 `data`：最近一条计划 + 过滤后明细（planDetailList[].assessDefineId/subGuideItemId、id）。注意路径大小写 `/item/List`。AI ✅。

### POST /periodical/plan/subGuideItem/list — 勾选项转计划明细
- 前端：`childApi.periodicalPlanSubGuideItemList`（periodicalRecord.vue、individualLesson.vue）
- 请求体：**数组** SubGuideItemVo[]：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| type | string | 是 | 1 评估推荐 / 2 机构 IEP 库 / 3 近期干预 |
| assessDefineId | string | type=1 必填 | 量表 id |
| subGuideItemIds | string[] | 是 | 勾选的子导项 id 集合 |

- 响应 `data`：统一结构列表（`item` 领域码、`subItem` 子项名、`assessDefineId`、`content`、`id`=subGuideItemId），前端映射为 planDetailList 元素。空数组→"请求参数错误"。AI ✅。

### GET /periodical/plan/info — 计划详情
- 前端：`childApi.periodicalPlanInfo`（periodicalRecord.vue、individualLesson.vue、courseRecord.vue）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| planId | query | string | **是** | 计划 id |

- 响应 `data`：TRecoverPeriodicalPlan：`id`、`name`、`childId/childName`、`fromDate/toDate`、`teacher/teacherName`、`planSummary`、`planDetailList[]`（`id`、`recoverItem/recoverSubItem`、`content`、`subGuideItemId`、`assessDefineId`）。AI ✅。

### POST /periodical/plan/saveOrUpdate — 新建/修改个训计划
- 前端：`childApi.saveOrUpdate`（individualLesson.vue submit；**函数名无模块前缀，实际是个训计划保存**）
- AI 网关：✅ 可调用

请求体 TRecoverPeriodicalPlan：

| 字段 | 类型 | 必填 | 前端来源 / 后端说明 |
|---|---|---|---|
| id | string | 更新必填 | 空=新增（服务端 UUID） |
| childId | string | 是 | 无康复过程记录→"儿童康复数据不存在" |
| childName | string | 否 | 前端传，便于展示 |
| name | string | 是 | 计划名称 |
| fromDate / toDate | string/时间戳 | 是 | 起止日期 |
| teacher | string | 否 | **后端强制 = 当前登录用户**，传了也无效 |
| planDetailList | Detail[] | 是 | **先删后插**：`{recoverItem, recoverSubItem, assessDefineId, content, subGuideItemId}` |
| status / type / rpId | — | 否 | 服务端强制：status="1" 草稿、type="01"、rpId 按 childId 自动查 |

- 响应：`{"code":200,"msg":"保存成功"}`。

### GET /periodical/record/list — 个训记录回显
- 前端：`childApi.periodicalRecordList`（periodicalRecord.vue、individualLesson.vue）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| planId | query | string | **是** | 计划 id |

- 响应 `data`：TRecoverLessonRecord 数组（`lessonResultCode`、`lessonDate`、`planDetailId`），仅返回 lessonResultCode 非空记录，按 lessonDate 倒序。AI ✅。

### POST /periodical/record/saveOrUpdate — 保存个训记录
- 前端：`childApi.periodicalRecordSaveOrUpdate`（periodicalRecord.vue、individualLesson.vue）
- AI 网关：✅ 可调用

请求体 PlanRecordVo：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| planId | string | 是 | 计划 id |
| planSummary | string | 否 | 计划总结（写入 plan.summray，注意拼写） |
| recordList | Record[] | 是 | **先删后插**（先删该计划全部旧记录）：`{lessonDate(yyyy-MM-dd), lessonResultCode(结果代码 P/PP/I…), planDetailId, teacherId}` |

- 响应：`{"code":200,"msg":"保存成功"}`。lessonResultCode 取值须来自 /periodical/record/type/list。
- ⚠️ 前端 individualLesson.vue:466-467 有硬编码测试值（lessonDate="2025-11-24"、lessonResultCode="pp"），是遗留代码，不要参考。

### GET /periodical/record/type/list — 记录代码选项
- 前端：`childApi.periodicalRecordTypeList`（periodicalRecord.vue）。无参数。
- 响应 `data`：TrainingRecord 数组（`value` 代码、`record` 中文名），status='1' 按 num 倒序。AI ✅。

### GET /periodical/year/page — 年度计划分页
- 前端：`childApi.periodicalYearPage`（course/itemRecord.vue）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| current | query | long | 否（默认1） | 每页固定 10 条 |
| date | query | string | 否 | **yyyy**（年份字符串，默认今年） |
| childName | query | string | 否 | 姓名模糊 |

- 响应 `data`：Page（TRecoverPeriodicalPlan，含 childName、teacherName、progress 如 "3/10"）。查询按当前用户为 teacher 过滤，年份取 fromDate 或 toDate 落在该年。AI ✅。

### POST /periodical/plan/delete — 删除个训计划
- 前端：`childApi.periodicalPlanDelete`（3 处）。请求体 `{"planId":"..."}`。
- AI 网关：❌ 禁止（删除禁令）。物理删除 记录→明细→计划。

## 三、训练统计（/training）

三个接口日期均为 query 必填 `yyyy-MM-dd`；查询范围=当前用户担任教师（个训 teacher=userId；组课为主/辅训老师）的课程。AI 均 ✅。

### GET /training/list — 当天课程
- 前端：`childApi.trainingList`（course.vue、AIassistant.vue）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| date | query | string | **是** | yyyy-MM-dd（前端格式化可能为 yyyy-M-d，AI 统一用 yyyy-MM-dd） |
| userId | query | string | 否 | 后端取 token 当前用户，前端传的 userId 被忽略 |

- 响应 `data`：`{startDate, endDate, userId, periodicalPlanList[]（个训）, teamPlanList[]（组课）}`；组课元素含 `scheduleDefineId`、`startDate`、`timeRange`、`repeatType`、`teamv3ParticipantList[].participantId/participantName`、`teamv3SchemeStepList[].employeeName/teacherType`。

### GET /training/today/count — 当天课程数
- 前端：`childApi.trainingtodayCount`。query：date（必填，yyyy-MM-dd）。响应 `data`：int（个训+组课）。

### GET /training/dateRange/count — 区间每日课程数
- 前端：`childApi.trainingDateRangeCount`（course.vue 周概览）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| startDate / endDate | query | string | **是** | yyyy-MM-dd |
| userId | query | string | 否 | 被后端忽略（取 token） |

- 响应 `data`：Map（key=yyyy-MM-dd，value=当天课程数）。注意：组课计数 SQL 未按 userId 过滤（已知行为）。

## 四、IEP 库（/iepLib）

### POST /iepLib/myIep/list — 我的 IEP 库
- 前端：`childApi.iepLibMyIepList`（myIEP.vue、addTrainingContent.vue）
- AI 网关：✅ 可调用。请求体 IepDetailVo：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| assessDefineId | string | 否 | 按 iepType=assessDefineId 精确过滤 |
| childId | string | 否 | 前端传，后端忽略 |
| content | string | 否 | 内容模糊（搜索词，默认 ""） |

- 后端强制 author=当前用户。响应 `data`：TRecoverPplandetailTeacherPref 数组（`id`、`recoverItemName`、`recoverItem`、`recoverSubItem`、`content`…）。
- 其他可用过滤：`item` 精确、`subItem` 模糊、`fromAge/toAge`（月龄区间）、`scope`。

### POST /iepLib/publicIep/list — 机构共享 IEP 库
- 前端：`childApi.iepLibPublicIepList`（institutionIEP.vue、addTrainingContent.vue）
- 同 myIep/list，但固定 scope="1"（共享），可传 `userId` 过滤作者。AI ✅。

### POST /iepLib/saveOrUpdate — 新建/修改 IEP 条目
- 前端：`childApi.iepLibSaveOrUpdate`（createdContent.vue 快捷创建、addMyIEP.vue 表单）
- AI 网关：✅ 可调用。请求体 TRecoverPplandetailTeacherPref：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| id | string | 更新必填 | 空=插入非空=更新 |
| recoverSubItem | string | 是 | 训练项目（子项）名称 |
| content | string | 是 | 训练内容 |
| author | string | 是 | 作者 employeeId（前端取当前用户） |
| recoverItem | string | addMyIEP 传 | 领域编码（如 VIM、OTHER） |
| recoverItemName | string | 否 | 领域名称 |
| iepType | string | addMyIEP 传 | 存 assessDefineId |
| fromAge / toAge | int | 否 | 适用月龄区间 |
| scope | string | 否 | 1共享 2私有 |

- 后端无字段校验（信任前端）；快捷创建只传 recoverSubItem/content/author 亦可。

## 前端未调用、后端存在的接口

| 接口 | 请求 | 说明 | AI |
|---|---|---|---|
| POST /iepLib/myIep/page | query current + IepDetailVo body | 我的 IEP 分页（每页 10） | ✅ |
| POST /iepLib/publicIep/page | 同上 | 共享 IEP 分页 | ✅ |
| POST /iepLib/more/saveOrUpdate | TRecoverPplandetailTeacherPref[] | 批量 upsert（id 空=插） | ✅ |
| GET /team/dateRange/list | 同 dateRange/page 但不分页 | 区间组课列表 | ✅ |
| GET /team/child/leave/list | query groupId | 已离组成员（status="3"） | ✅ |
| GET /team/scheme/list、/common/list、/all/list | SchemeVo body | 机构库/共享库/双库列表（all 返回 SchemeDTO 两组） | ✅ |
| POST /team/scheme/common/page、/all/page | query current + SchemeVo body | 对应分页 | ✅ |
| GET /team/scheme/level/map | 无 | 等级码→名称（lowfunction 低功能等） | ✅ |
| GET /team/lesson/summary/info/list | — | 快照收录，源码未见独立实现 | — |
| GET /periodical/year/list | query date(yyyy)/childName | 年度计划不分页版 | ✅ |
| POST /periodical/plan/detail/list | — | 快照收录 | — |

## 枚举与常量

- 重复类型 repeatType：`0` 不重复、`1` 每日、`2` 每周、`3` 每月、`4` 隔天、`5` 工作日（每周按周一=1…周日=7；每月开始日为 31 号时取月末；隔天=与开始日间隔为偶数）。
- 日程类型 scheduleType：0评估 1组训 2个训 3考勤 4自定义（组课保存固定 "1"）。
- teacherType：`1` 主训、`2` 辅训。participantType：`0` 儿童个人、`1` 儿童组（组课保存强制 "1"）、`-1` 排除儿童。
- 出勤 present：`0` 请假、`1` 到场、`2` 缺席。assignStatus：`0` 完成、`1` 跳过。
- 小组状态：`1` 有效/`0` 无效；成员状态 1排队 2在组 3退组。
- 个训计划 status：`1` 草稿（保存强制）、`2` 已审核/生效、`3` 结束；type 固定 "01"。
- IEP 来源 SubGuideItemVo.type：`1` 评估推荐、`2` 机构 IEP 库、`3` 近期干预。
- IEP scope：`1` 共享、`2` 私有。教案等级：lowfunction/middlefunction/hignfunction（注意 hign 拼写）。
- 总结评分落位：summary/type 的 `extra2`=0→`score0`、1→`score1`，依次到 score9。
- 教案类型/总结类型：字典 `teamCourceSchemeType` / `teamSummaryType`（sys_basedata，运行时数据）。
