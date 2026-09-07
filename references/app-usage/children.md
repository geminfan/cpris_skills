# 儿童档案模块（/childrenInfo/*）实际调用接口

Controller：`ChildrenInfoController.java`（cpris_wxapp/children）。前端函数均在 `childApi`。除特别说明外，AI 网关 service=children，路径 `/ai/gw/children/childrenInfo/...`。

## 前端有调用点的接口

### GET /childrenInfo/page — 儿童分页
- 前端：`childApi.childPage`（childPage.vue 列表/搜索）
- AI 网关：✅ 可调用

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| current | query | long | 否（默认1） | 页码，每页固定 10 条 |
| name | query | string | 否 | 儿童姓名，模糊匹配 |
| status | query | string | 否 | 2已登记 / 5已入训 / 9已离训；前端固定传 `""` |

- 响应 `data`：Page；records 元素为 TChildrenInfo（含回填 `statusName`、`rpId`）。
- 后端限制：固定限定 `status IN (2,5,9)`（离训儿童也在内）；按创建时间倒序；机构隔离取 token。找特定儿童建议带 `name` 一次命中，避免全量翻页。

### POST /childrenInfo/list — 儿童列表（不分页）
- 前端：`childApi.childrenInfoList`（chooseChildren.vue：选儿童 status="5"；groupChildren.vue：候选儿童带 elseChildIds）
- AI 网关：✅ 可调用

请求体 ChildListVo：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| name | string | 否 | 姓名模糊匹配 |
| status | string | 否 | "5"=已入训（选儿童场景），""=全部 |
| elseChildIds | string[] | 否 | 排除的儿童 id（已在组儿童） |

- 响应 `data`：TChildrenInfo 数组（含 statusName、rpId）。
- 后端限制：**body 必须传 JSON 对象**（`@RequestBody(required=false)` 但代码直接 `.getName()`，传 null 会 NPE/500）；结果为空时对空 childIds 拼 `IN ()` 依赖 MP 版本行为。前端 chooseChildren 额外传 `current:1`，后端忽略。

### GET /childrenInfo/info — 儿童详情
- 前端：`childApi.childInfo`（createChild.vue 编辑回显）
- AI 网关：✅ 可调用

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| childId | query | string | **是** | 儿童 id |

- 响应 `data`：TChildrenInfo + `childrenVisitList`（1 条，含 `jdzName` 接待者姓名；无记录时为 `[null]`）+ `childrenGuardianList`（1 条，`phone` 是否脱敏以当前账号权限和实际返回为准）。
- 后端限制：返回的是只读拼装结果，**不能整体回传给 saveOrUpdate**（见坑清单第 2 条）。

### GET /childrenInfo/common/info — 儿童常用信息
- 前端：`childApi.childrenInfoCommonInfo`（评估相关 6 个页面）
- AI 网关：✅ 可调用

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| childId | query | string | **是** | 儿童 id |

- 响应 `data`：`{name, sex(中文"男孩/女孩"), age}`。childId 无效时后端 NPE（500）。

### GET /childrenInfo/checkName — 重名校验
- 前端：`childApi.childrenInfoCheckName`（createChild.vue 提交前）
- AI 网关：✅ 可调用

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| name | query | string | **是** | 儿童姓名，精确匹配（trim 后） |

- 响应 `data`：`true` 有重名。注意：saveOrUpdate **不强制**重名校验，仅前端预检。

### GET /childrenInfo/count — 在训儿童数
- 前端：`childApi.childrenInfoCount`（course.vue 统计卡）
- AI 网关：✅ 可调用。无参数。响应 `data`：int，固定统计 `status="5"`。

### GET /childrenInfo/zdmc/list — 诊断名称列表
- 前端：`childApi.childrenInfoZdmcList`（createChild.vue 诊断下拉）
- AI 网关：✅ 可调用（路径首段为 childrenInfo，不受 blockedPrefixes 影响）。无参数。
- 响应 `data`：SysBasedata 数组（`text`/`value`），来源 sys_basedata `dataType="bzfl"`，按 displayOrder 升序。

### GET /childrenInfo/region/list — 行政区划联动
- 前端：`childApi.childrenInfoRegionList`（createChild.vue 省市区三级）
- AI 网关：✅ 可调用

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| parentId | query | string | 否（默认"1"） | 上级区划 id；"1"=省级，逐级下钻 |

- 响应 `data`：TRegion 数组（`regionId`、`regionName`…）。前端保存儿童时 province/city/street 存的是 **regionName**。

### POST /childrenInfo/saveOrUpdate — 新建/修改儿童
- 前端：`childApi.childrenInfoSaveOrUpdate`（createChild.vue）
- AI 网关：✅ 可调用

请求体 TChildrenInfo（前端实际只传下列字段）：

| 字段 | 类型 | 必填 | 前端来源 / 后端说明 |
|---|---|---|---|
| childId | string | 更新必填 | 无=新建（服务端生成 UUID），有=按 id updateById（null 字段不覆盖） |
| name | string | 是 | 姓名 |
| sex | string | 是 | "M" 男孩 / "F" 女孩 |
| birthday | string/时间戳 | 是 | 出生日期 |
| province/city/street | string | 否 | 户籍地（前端存 regionName） |
| childrenVisitList | TChildrenVisit[] | 新建建议必带 | 至少 `[{jdrq:接待日期, zdmc:诊断名称, jdz:接待教师employeeId}]`；**先删后插** |
| childrenGuardianList | TChildrenGuardian[] | 否 | `[{phone:手机号}]`；**先删后插**；更新时须传完整列表 |
| 其余 TChildrenInfo 字段 | — | 否 | 见下方实体表；status 由服务端强制 "2"（已登记），不能经此接口入训 |

- 响应：`{"code":200,"msg":"保存成功"}`。
- 后端约束（`TChildrenInfoServiceImpl.saveOrUpdateAndVisitAndRp`，@Transactional）：
  - status 强制置 "2"；儿童无康复过程记录时自动新建（rpId=UUID）。
  - childrenVisitList / childrenGuardianList 非空才"先删后插"，传 `[null]` 会 NPE→500。
  - jdrq 支持 ISO-8601 字符串或毫秒时间戳，AI 优先毫秒时间戳。

TChildrenInfo 完整字段（更新可写字段，null 不覆盖）：

| 字段 | 类型 | 说明 |
|---|---|---|
| childId / name / sex / birthday | String/String/String/Date | 主键、姓名、M/F、生日 |
| onlyChild | String | 1是 0否 |
| province / city / street / district | String | 户籍地 |
| eduStatus / homeAddress / familyStructure / photo | String | 就读情况、住址、家庭结构、照片 |
| nickname / formerName | String | 小名、曾用名（逗号隔开） |
| namePinyin / nickNamePinyin / formerNamePinyin | String | 对应拼音 |
| nation / barcode / idcard / socialSecurityNo | String | 民族、条码、身份证、社保号 |
| disabilityCertificateNo / clinicNumber / hospitalizationNumber | String | 残疾证号、门诊号、住院号 |
| label / remark | String | 标签、备注 |
| isHospital | String | 0门诊 1住院 |
| isfast | String | 0否 1快速建档评估 2快速建档入训 |
| trainType | String | changguiruxun/duanqiruxun/zhuyuanruxun（入训接口写入） |
| cjlb | String | 残疾类别 |
| status | String | 2/5/9（此接口强制 2） |
| dg*、etl* | — | 审计/ETL 字段，服务端管理，不要传 |

TChildrenVisit（接待记录）关键字段：`visitId`（主键，服务端生成）、`zdmc` 诊断名称（取 bzfl 字典 text）、`jdz` 接待者 employeeId、`jdrq` 接待日期、`jddx/sfxdet/gcjl/clzt/kfzz/ghbz/qtzz/fzxm/jy/cl` 等观察字段、`rpId`、`childId`、返回时附 `jdzName`。

TChildrenGuardian（监护人）关键字段：`guardianId`（主键）、`childId`、`name`、`relation`（父亲/母亲/监护人）、`phone`、`qq`、`weixin`、`degree`、`job`、`ageRange`、`email`、`birthday`、`displayOrder`。查询返回的 phone 是否脱敏以当前账号的 ai_show_child_phone 权限和实际返回为准；若返回掩码，不得将其回写或猜测还原。仅更新获授权的字段；必须提交完整监护人列表却缺少真实号码时，请用户补充，不能用掩码覆盖原值。

### POST /childrenInfo/enterTraining — 儿童入训
- 前端：`childApi.childrenInfoEnterTraining`（invalidChild.vue 入训保存）
- AI 网关：✅ 可调用

请求体 EnterTrainingVo：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| childId | string | 是 | 儿童 id（无康复过程记录会 NPE） |
| enterDate | string | 否 | yyyy-MM-dd，不传默认当前时间 |
| enterType | string | 是 | 入训类别（sys_basedata rxlb 字典 value，如 changguiruxun） |
| teacher | string | 是 | 主训老师 employeeId |
| enterGroupIds | string[] | 否 | 入组小组 id；**null 会 NPE**，不用组传 `[]` |

- 响应：`{"code":200,"msg":"入训成功"}`。
- 后端约束：小组差集处理（已在该组的跳过）；更新康复过程 rpStatus="5"、assignTeacher、enterDate，新增转师记录；儿童 status 置 "5"、trainType=enterType。

### POST /childrenInfo/delete — 删除儿童全部信息
- 前端：`childApi.childrenInfoDelete`（childPage.vue）。请求体 `{"childId":"..."}`。
- AI 网关：❌ 禁止（删除禁令）。后端为级联物理删除（成长/行为/接待/监护人/评估/个训/报告文件等 16 类），无前置校验。

## 前端未调用、但可用的接口（后端约束简述）

| 接口 | 请求 | 后端约束/说明 | AI |
|---|---|---|---|
| POST /childrenInfo/visit/saveOrUpdate | TChildrenVisit JSON | visitId 空=插入（UUID 自动生成），非空=更新。补录接待日期用它：`{"childId":"...","jdrq":<毫秒时间戳>}`（known-issues 已验证） | ✅ |
| POST /childrenInfo/guardian/saveOrUpdate | TChildrenGuardian[] JSON | MP saveOrUpdateBatch：guardianId 空=插入非空=更新，**不校验 childId 归属** | ✅ |
| POST /childrenInfo/growth/saveOrUpdate | TChildrenRegGrowth JSON | growthId 空=插入。字段：yybd/yylj/rznl/sjnl/shzl（言语表达/语言理解/认知/社交/生活自理）+ childId/rpId | ✅ |
| POST /childrenInfo/behavior/saveOrUpdate | TChildrenRegBehavior JSON | behaviorId 空=插入。字段：kbxw 刻板行为、gddyldx 固定依赖对象、zxhdwj 最喜欢玩具、sftx 是否挑食、zxhdsw/zxhdhd/zhpdsw、gjphxw 攻击破坏行为、smqk 睡眠 | ✅ |
| POST /childrenInfo/history/record/saveOrUpdate | ChildrenRecordDTO | `{diagnoseRecordList, recoverRecordList, aidRecordList}` 三类历史记录逐条 upsert（recordId 空=新增），无先删后插 | ✅ |
| POST /childrenInfo/image/saveOrUpdate | TChildrenImage[] | `{imageId,imageDesc,imagePath,childId}`，批量 upsert | ✅ |
| GET /childrenInfo/enterTraining/info | query childId（必填） | 返回 `{trainType, teacherId, enterDate}`；rpId 链路有已知缺陷，childId 不存在可能 500 | ✅ |
| GET /childrenInfo/nation/list | 无 | 民族列表 t_nation | ✅ |
| GET /childrenInfo/rxlb/get | 无 | 返回 `{"rxlb":[SysBasedata...]}` 入训类别字典 | ✅ |

## 枚举与常量

- 儿童状态 status：`2` 已登记、`5` 已入训、`9` 已离训；列表固定过滤 `IN (2,5,9)`。
- 性别 sex：`M` 男孩、`F` 女孩（common/info 返回中文）。
- 入训类别 trainType/enterType：`changguiruxun` 常规、`duanqiruxun` 短期、`zhuyuanruxun` 住院（字典 rxlb）。
- 诊断名称 zdmc：字典 `bzfl`。
- 小组成员状态：`1` 排队、`2` 在组、`3` 退组。
- 康复过程 rpStatus 与儿童 status 同步（2/5/9）。
