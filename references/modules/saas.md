# saas 模块 REST 接口

共 20 个已识别接口。

本模块为静态接口资料；调用资格见表末列，具体约束见 [网关契约](../gateway-contract.md)。

## 接口列表

| 方法 | 路径 | 功能 | Controller | 详情  AI 调用 |
|---|---|---|---|---|---|
| GET | `/auth/list` | 查询列表 | `DataController` | [getAuthMap](../interfaces/get-auth-list-getauthmap.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| GET | `/data/map` | GET /data/map | `DataController` | [getAssessItemsMap](../interfaces/get-data-map-getassessitemsmap.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| GET | `/files/assess/{merchantId}/{uuid}/{fileName}/{ticket}` | GET /files/assess/{merchantId}/{uuid}/{fileName}/{ticket} | `DataController` | [getAssessReportFile](../interfaces/get-files-assess-merchantid-uuid-filename-ticket-getassessreportfile.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| GET | `/files/signature/{merchantId}/{uuid}/{fileName}/{ticket}` | GET /files/signature/{merchantId}/{uuid}/{fileName}/{ticket} | `DataController` | [getSignatureImage](../interfaces/get-files-signature-merchantid-uuid-filename-ticket-getsignatureimage.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| GET | `/nation/list` | 查询列表 | `DataController` | [getNationList](../interfaces/get-nation-list-getnationlist.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| GET | `/region/list` | 查询列表 | `DataController` | [getRegionList](../interfaces/get-region-list-getregionlist.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| GET | `/sysBasedata/list` | 查询列表 | `DataController` | [getKinshipList](../interfaces/get-sysbasedata-list-getkinshiplist.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| POST | `/login` | 登录 | `LoginController` | [login](../interfaces/post-login-login.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| POST | `/loginOut` | 登录 | `LoginController` | [loginOut](../interfaces/post-loginout-loginout.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| POST | `/phone/bind` | 绑定 | `LoginController` | [bindPhone](../interfaces/post-phone-bind-bindphone.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| GET | `/phone/findPassword` | GET /phone/findPassword | `LoginController` | [getPhoneNoFindPassword](../interfaces/get-phone-findpassword-getphonenofindpassword.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| POST | `/phone/login/merchant/list` | 查询列表 | `LoginController` | [getLoginMerchantMapByPhoneSms](../interfaces/post-phone-login-merchant-list-getloginmerchantmapbyphonesms.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| POST | `/phone/login/merchant/verify` | 登录 | `LoginController` | [verifyMerchant](../interfaces/post-phone-login-merchant-verify-verifymerchant.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| GET | `/phone/sms` | GET /phone/sms | `LoginController` | [getPhoneSms](../interfaces/get-phone-sms-getphonesms.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| POST | `/phone/updatePassword` | POST /phone/updatePassword | `LoginController` | [updatePassword](../interfaces/post-phone-updatepassword-updatepassword.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| POST | `/wx/bind` | 绑定 | `LoginController` | [wxBind](../interfaces/post-wx-bind-wxbind.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| POST | `/wx/login` | 登录 | `LoginController` | [wxLogin](../interfaces/post-wx-login-wxlogin.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| GET | `/wx/verify` | 校验 | `LoginController` | [wxVerify](../interfaces/get-wx-verify-wxverify.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| POST | `/parent/phone/login` | 登录 | `ParentLoginController` | [phoneLogin](../interfaces/post-parent-phone-login-phonelogin.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
| POST | `/parent/wx/login` | 登录 | `ParentLoginController` | [wxLogin](../interfaces/post-parent-wx-login-wxlogin.md)  不可调用：SaaS/登录/数据接口仅供源码参考 |
