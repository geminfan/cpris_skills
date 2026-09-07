# 用户与登录模块（/user、/login、/phone、/wx、/auth、/sysBasedata）实际调用接口

Controller：`UserController`（/user）、`LoginController`（无前缀，登录族）、`DataController`（无前缀，字典/权限/文件）。

**AI 网关注意**：本模块除 `/user/*` 外全部在 blockedPrefixes（login、loginOut、phone、wx、auth、data、sysBasedata、nation、region、files），**仅前端可调**，AI 智能体不能也不需要调用（AI 网关有自己的 X-Api-Key 认证）。以下文档用于理解前端行为与字段语义；`/user/info` 是 AI 网关 login 校验使用的接口。

## 一、用户信息（/user，AI 网关 ✅）

### GET /user/info — 当前用户信息
- 前端：`childApi.userInfo`（login.vue 登录后、selectionInstitution.vue、myInfo.vue）
- AI 网关：✅ 可调用（login 验证即用它）。无参数，取 token 当前用户。

- 响应 `data`：TEmployee + 回填 `merchantId`、`merchantName`。前端常用：`name`、`employeeId`、`photo`、`sex`、`phone`、`enterDate`。注意 password 字段查询不返回（hidden）。

### GET /user/list — 员工列表
- 前端：`childApi.userList`（selectTeach.vue 选教师；login.vue 有方法未用）

| 参数 | 位置 | 类型 | 必填 | 说明 |
|---|---|---|---|---|
| name | query | string | 否 | 员工姓名模糊匹配 |
| status | query | string | 否 | 在职状态精确匹配（前端传 "1"） |

- 响应 `data`：TEmployee 数组（前端取 `employeeId`、`name`）。AI ✅。

### POST /user/update — 修改当前用户资料
- 前端：`childApi.userUpdate`（myInfo.vue saveForm）
- AI 网关：✅ 可调用

请求体 TEmployee（前端实际传）：

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| photo | string | 否 | 头像地址；**后端强制置 null 不生效**，改头像必须走 /user/avatar/save |
| name / sex / phone | string | 否 | 姓名/性别/手机 |
| enterDate | string/时间戳 | 否 | 入职日期 |

- 后端约束：employeeId 强制 = 当前登录用户（**只能改自己**，body 里的 employeeId 被忽略）；updateById 忽略 null 字段。

### POST /user/avatar/save — 上传头像（multipart）
- 前端：`childApi.userAvatarSave` 定义了但页面用 `uni.uploadFile` 直传 `baseURL + "/user/avatar/save"`，文件字段名 `file`，Header 带 Bearer token。
- AI 网关：需 multipart 调用方（cpris_auth.py 不支持 multipart）。
- 后端行为：先递归删除旧头像目录再上传；返回 `msg`=相对路径 `files/avatar/{merchantId}/{userId}/{uuid}/{uuid}.{ext}`，前端拼 `baseURL + "/" + msg` 展示。

## 二、登录族（❌ AI 网关禁止，仅前端）

### POST /login — 账号密码登录
- 前端：`userApi.login`（login.vue）
- 请求体 LoginVo：`username`（t_employee.employee_id）、`password`（明文，服务端加盐 MD5）、`merchantId`（机构代码）。三者必填。
- 响应 `data`：`{accessToken, expiresIn, endDate}`；前端存 `Bearer {accessToken}`。失败文案："机构代码或账号错误"、"账号或密码错误"、"机构已过期"、"账号已禁用（离职用户）"。

### GET /phone/sms — 发送短信验证码
- 前端：`childApi.phonesms`（login.vue、forgotPassword.vue）
- query：`phone`（必填，trim）。4 位数字验证码，**300 秒有效**；同一手机号 60 秒 1 次、每日 50 次。返回 `{"code":200,"msg":"验证码发送成功"}`。

### POST /phone/login/merchant/list — 验证码登录：取机构列表
- 前端：`childApi.phoneLoginMerchantList`（login.vue、selectionInstitution.vue、forgotPassword.vue）
- 请求体：`{phoneNo, smsCode}`。
- 响应 `data`：`[{merchantId, name}]`；恰 1 个机构前端自动 verify，多个跳选机构页。

### POST /phone/login/merchant/verify — 验证码登录：选定机构换 token
- 前端：`childApi.phoneLoginMerchantVerify`（login.vue、selectionInstitution.vue）
- 请求体：`{phoneNo, smsCode, merchantId}`（此处 merchantId 来自请求体）。
- 响应 `data`：AccessToken（同 /login）。验证码校验通过后立即作废（一次性）。

### POST /loginOut — 退出登录
- 前端：`childApi.loginOut`（my.vue）。无参数；带 Authorization 头则删服务端 Redis 权限 key，前端清本地 token。

### POST /phone/updatePassword — 密码重置
- 前端：`childApi.phoneUpdatePassword`（setNewPassword.vue）
- 请求体：`{merchantId, phoneNo, smsCode, password}`（新密码明文）。成功后同步更新 t_employee 与 t_public_user 密码（加盐 MD5：`MD5(明文+"{ZnO39yZwS3gCX7hi}")`）。

### GET /wx/verify — 微信 code 换 openid
- 前端：`childApi.wxVerify`（login.vue getOpenId，uni.login 的 code）
- query：`code`（必填）。响应 `data.wxOpenid`；服务端写 Redis `wx:{openid}` 5 分钟一次性凭证（供 /wx/login 用，前端当前未调用 /wx/login）。

## 三、权限与字典（❌ AI 网关禁止）

### GET /auth/list — 当前用户权限码集合
- 前端：`userApi.authList`（utils/store/index.js fetchPermissions）
- 无参数。响应 `data`：权限码 Set；前端存 Vuex/Storage，`hasPermission` 判断，含 `'admin'` 表示超管。空集合→"数据不存在"。

### GET /sysBasedata/list — 基础数据字典
- 前端：`childApi.sysBasedataList`（invalidChild.vue）
- query：`dataTypes`（**List，必填**，可重复：`dataTypes=rxlb&dataTypes=bzfl`）。
- 响应 `data`：Map（key=dataType，value=SysBasedata 数组）。已知 dataType：`rxlb` 入训类别、`bzfl` 诊断名称、`teamSummaryType` 组训总结类型、`teamCourceSchemeType` 教案类型。

## 前端未调用、后端存在的接口

| 接口 | 请求 | 说明 | AI |
|---|---|---|---|
| GET /user/page | query current/name/status | 员工分页（每页 10） | ✅ |
| GET /phone/findPassword | **GET + JSON body**（merchantId、username） | 返回密保手机号明文；HTTP 客户端需支持 GET 带 body | ❌ |
| POST /phone/bind | {phoneNo, smsCode}（需登录） | 只更新 t_public_user.phone_no，不同步 t_employee.phone；手机已绑其他账号会拒绝 | ❌ |
| POST /wx/bind | {wxOpenid}（需登录） | 绑定微信；openid 已绑其他账号会拒绝 | ❌ |
| POST /wx/login | {wxOpenid} | 微信 openid 登录（依赖 /wx/verify 的 5 分钟凭证） | ❌ |
| GET /data/map | query dataId（必填） | XML 数据缓存（如 assess.getAssessType、training.getSchemeLevel） | ❌ |
| GET /nation/list、/region/list | 无 / parentId | 与 /childrenInfo/nation|region/list 等价的独立入口 | ❌ |
| GET /files/assess/{merchantId}/{uuid}/{fileName}/{ticket} | 路径变量 | 评估报告文件下载（免登录，ticket 5 分钟有效）；物理路径 user.dir/files/assess/... | ❌ |
| GET /files/signature/{merchantId}/{uuid}/{fileName}/{ticket} | 路径变量 | 签名图片下载（同上） | ❌ |

## 登录链路摘要（前端视角）

1. 账号密码：`POST /login` → accessToken（subject=`merchantId#userId`，权限写 Redis `jwt:{merchantId}#{userId}`）。
2. 短信：`GET /phone/sms` → `POST /phone/login/merchant/list`（多机构时用户选）→ `POST /phone/login/merchant/verify` → accessToken。
3. token 过期：任意接口返回 `data.error="invalid_token"` 或 `code=401` → 前端清 token 跳登录页。
4. AI 智能体不走此链路：用 X-Api-Key 经 AI 网关，网关内部代换 JWT；仅需 `/user/info` 校验密钥。
