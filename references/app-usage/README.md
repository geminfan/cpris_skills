# 教师微信端（xipuApp2）实际调用接口手册

依据前端工程 `xipuApp2`（uni-app，接口集中在 `api/index.js` 的 `childApi`/`userApi`）与后端工程 `cpris_wxapp` 源码静态梳理。本手册覆盖前端**实际有调用点**的 84 个接口：前端每个调用点传入的字段、后端参数绑定、必填规则、格式要求、业务约束与已知坑。给 AI 智能体构造 / 核对请求用，比 `interfaces/` 骨架文档更完整；两者冲突时以本手册为准并按源码复核。

模块文档：

| 文件 | 范围 | 前端调用接口数 |
|---|---|---:|
| [children.md](children.md) | 儿童档案（/childrenInfo/*） | 11 |
| [assess.md](assess.md) | 评估（/assess、/assessDefine、/assessGuide、/assess/cars、/assess/mte1） | 31 |
| [training.md](training.md) | 训练（/team、/periodical、/training、/iepLib） | 30 |
| [user-auth.md](user-auth.md) | 用户与登录（/user、/login、/phone、/wx、/auth、/sysBasedata、/data） | 12 |

`api/index.js` 中定义但前端无调用点的函数（29 个）在各模块文档末尾列出，AI 调用前需自行确认业务语义。

## 全局调用约定

### 地址与认证

| 端 | 地址 | 认证 |
|---|---|---|
| 前端 App（业务网关） | test `http://test.cpris.com` / prod `https://teacherwx.cpris.com` | `Authorization: Bearer {accessToken}`（/login 或 /phone/login/merchant/verify 返回） |
| AI 智能体 | test `http://testai.cpris.com` / prod `https://aiskills.cpris.com`，路径 `{ai网关}/ai/gw/{service}/{业务路径}` | 仅 `X-Api-Key`，见 [网关契约](../gateway-contract.md) |

service 映射：`/childrenInfo`→children；`/assess*`→assess；`/team`、`/periodical`、`/training`、`/iepLib`→training；`/user`→user。登录、短信、微信、字典、文件前缀（login、loginOut、phone、wx、auth、data、files、nation、region、sysBasedata）在 AI 网关 blockedPrefixes 中，**仅前端可调**。

### 响应包装

所有接口返回 `R<T>`：`{"code":200,"msg":"成功","data":...}`。code=200 才是成功；前端只判断 `result.code == 200`。401/`invalid_token` 表示登录过期。注意个别接口把业务数据放在 `msg`（如 `/assess/saveOrUpdate` 的 msg=评估id、`/assess/report/summary/*` 的 msg/info=简述文本）。

### 分页

分页接口统一 `current`（默认 1）+ **固定每页 10 条**（Controller 内 `new Page<>(current, 10L)`，前端无法改 size）。返回 MyBatis-Plus Page：`records[]`、`total`、`size`、`current`、`pages`。`POST /team/scheme/*` 的 `current` 是 **query 参数**而非 body 字段，其余 POST 分页（如 /childrenInfo/list）不分页。

### 日期格式

| 场景 | 格式 | 说明 |
|---|---|---|
| Query 日期参数（后端 hutool 解析） | `yyyy-MM-dd`（/periodical/year/* 为 `yyyy`） | 前端部分页面传 `yyyy-M-d`（宽松解析可用），AI 调用统一用 `yyyy-MM-dd` |
| JSON Body 日期字段 | 毫秒时间戳最稳；或 ISO-8601 字符串 | 无全局 @JsonFormat；`VSmdAssess.assessDate/assessAppointDate` 标注 `yyyy-MM-dd HH:mm:ss`，前端实际传 `yyyy-MM-dd HH:mm` 亦可 |
| `timeRange`（组课时间段） | `HH:mm~HH:mm` | 按 `~` 拆分，如 `08:00~09:00` |

### 机构隔离与权限

- 已登录接口的机构由 **token subject（`merchantId#userId`）** 决定（`MerchantContextHolder`/`UserContextHolder`），请求体不传 merchantId；例外：`/phone/login/merchant/verify`、`/phone/findPassword`、`/phone/updatePassword` 未登录，merchantId 取请求体。
- 数据层按 `@DB("merchant")` 路由机构库；教案"机构专属库 / 共享库"即 merchant 库 / common 库。
- 后端每个方法有 `@PreAuthorize("@perm.has('权限码')")`，权限码 = 机构套餐功能 ∩ 用户角色权限；权限不足返回 403。
- 只能改自己的数据：`/user/update` 强制 `employeeId=当前用户`；`/periodical/plan/saveOrUpdate` 强制 `teacher=当前用户`；`/iepLib/myIep/*` 强制 `author=当前用户`。

## 高频坑清单（跨模块）

1. **先删后插（全量替换语义）**，漏传即丢数据，禁止传 `[null]`：
   - `POST /childrenInfo/saveOrUpdate` 的 `childrenVisitList`、`childrenGuardianList`
   - `POST /team/lesson/saveOrUpdate`（修改时参与人/教案步骤/assign 全部重插）
   - `POST /periodical/plan/saveOrUpdate` 的 `planDetailList`
   - `POST /periodical/record/saveOrUpdate` 的 `recordList`（先删该计划全部旧记录再重插）
   - `POST /team/lesson/summary/saveOrUpdate` 的 `teamLessonV2RpList`
   - `POST /assess/cars/result/saveOrUpdate`、`POST /assess/mte1/result/saveOrUpdate`（教师卷/家长卷答案）
2. **更新走"非空覆盖"**：MyBatis-Plus `updateById` 忽略 null 字段，因此更新只需最小请求体（如改名只传 `childId`+`name`）。不要把查询结果整体回传：详情接口返回的 `childrenVisitList:[null]` 占位、监护人脱敏手机号（`152****6412`）、审计字段回写都会污染数据或 500。
3. **评估 id 键名三种写法**：`/assess/saveOrUpdate` 用 `entityid`；`/assess/result/saveOrUpdate` 用 `entityId`；`/assess/result/item/saveOrUpdate` 用 `assessEntityid`。填错后端收不到值。
4. **新建儿童必须带接待日期**：`childrenVisitList:[{"jdrq":...}]`，否则无接待记录；详见 [known-issues.md](../known-issues.md)。
5. **新建评估必须带全业务字段**：`assessDate`、`assessAppointDate`、`employeeId`、`assessType`（能力评估为 `"1"`）缺一不可，`dgCreatedDate/dgCreatedBy` 只是审计字段。
6. **删除类路径 AI 网关一律禁止**（含 POST /assess/delete、/childrenInfo/delete、/periodical/plan/delete、/team/lesson/delete、/team/lesson/onlyOne/delete），前端专用。
7. **`objValue` 哨兵值 `"xxxxx"`** 表示未填写；问卷完成状态判定（/assess/result/status/map）遇到它即判未完成。
8. **前端遗留问题**（写文档时已知，AI 不应模仿）：`individualLesson.vue:466-467` 的 recordList 中 lessonDate/lessonResultCode 为硬编码测试值；`childApi.saveOrUpdate` 函数名易误导，实际是 `/periodical/plan/saveOrUpdate`。

## 源码定位

- 前端：`xipuApp2/api/index.js`（接口定义）、`utils/request.js`（请求封装：GET 参数走 query，POST 走 JSON body，超时 15s，401 跳登录）、`config/env.js`（baseURL）。
- 后端：`cpris_wxapp/{children,assess,training,user,saas}/src/main/java/com/cpris/controller/*.java`；实体在 `common/src/main/java/com/cpris/api/domain/`。行号为 2026-09 快照。
