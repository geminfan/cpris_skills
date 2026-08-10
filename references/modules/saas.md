# saas 模块 REST 接口

共 20 个已识别接口。

## 接口列表

| 方法 | 路径 | 功能 | Controller | 详情 |
|---|---|---|---|---|
| GET | `/auth/list` | 查询列表 | `DataController` | [getAuthMap](../interfaces/get-auth-list-getauthmap.md) |
| GET | `/data/map` | GET /data/map | `DataController` | [getAssessItemsMap](../interfaces/get-data-map-getassessitemsmap.md) |
| GET | `/files/assess/{merchantId}/{uuid}/{fileName}/{ticket}` | GET /files/assess/{merchantId}/{uuid}/{fileName}/{ticket} | `DataController` | [getAssessReportFile](../interfaces/get-files-assess-merchantid-uuid-filename-ticket-getassessreportfile.md) |
| GET | `/files/signature/{merchantId}/{uuid}/{fileName}/{ticket}` | GET /files/signature/{merchantId}/{uuid}/{fileName}/{ticket} | `DataController` | [getSignatureImage](../interfaces/get-files-signature-merchantid-uuid-filename-ticket-getsignatureimage.md) |
| GET | `/nation/list` | 查询列表 | `DataController` | [getNationList](../interfaces/get-nation-list-getnationlist.md) |
| GET | `/region/list` | 查询列表 | `DataController` | [getRegionList](../interfaces/get-region-list-getregionlist.md) |
| GET | `/sysBasedata/list` | 查询列表 | `DataController` | [getKinshipList](../interfaces/get-sysbasedata-list-getkinshiplist.md) |
| POST | `/login` | 登录 | `LoginController` | [login](../interfaces/post-login-login.md) |
| POST | `/loginOut` | 登录 | `LoginController` | [loginOut](../interfaces/post-loginout-loginout.md) |
| POST | `/phone/bind` | 绑定 | `LoginController` | [bindPhone](../interfaces/post-phone-bind-bindphone.md) |
| GET | `/phone/findPassword` | GET /phone/findPassword | `LoginController` | [getPhoneNoFindPassword](../interfaces/get-phone-findpassword-getphonenofindpassword.md) |
| POST | `/phone/login/merchant/list` | 查询列表 | `LoginController` | [getLoginMerchantMapByPhoneSms](../interfaces/post-phone-login-merchant-list-getloginmerchantmapbyphonesms.md) |
| POST | `/phone/login/merchant/verify` | 登录 | `LoginController` | [verifyMerchant](../interfaces/post-phone-login-merchant-verify-verifymerchant.md) |
| GET | `/phone/sms` | GET /phone/sms | `LoginController` | [getPhoneSms](../interfaces/get-phone-sms-getphonesms.md) |
| POST | `/phone/updatePassword` | POST /phone/updatePassword | `LoginController` | [updatePassword](../interfaces/post-phone-updatepassword-updatepassword.md) |
| POST | `/wx/bind` | 绑定 | `LoginController` | [wxBind](../interfaces/post-wx-bind-wxbind.md) |
| POST | `/wx/login` | 登录 | `LoginController` | [wxLogin](../interfaces/post-wx-login-wxlogin.md) |
| GET | `/wx/verify` | 校验 | `LoginController` | [wxVerify](../interfaces/get-wx-verify-wxverify.md) |
| POST | `/parent/phone/login` | 登录 | `ParentLoginController` | [phoneLogin](../interfaces/post-parent-phone-login-phonelogin.md) |
| POST | `/parent/wx/login` | 登录 | `ParentLoginController` | [wxLogin](../interfaces/post-parent-wx-login-wxlogin.md) |
