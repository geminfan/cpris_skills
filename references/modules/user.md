# user 模块 REST 接口

共 5 个已识别接口。

本模块为静态接口资料；调用资格见表末列，具体约束见 [网关契约](../gateway-contract.md)。

## 接口列表

| 方法 | 路径 | 功能 | Controller | 详情  AI 调用 |
|---|---|---|---|---|---|
| POST | `/user/avatar/save` | POST /user/avatar/save | `UserController` | [saveAvatar](../interfaces/post-user-avatar-save-saveavatar.md)  需授权及 multipart 调用方，JSON 脚本不支持 |
| GET | `/user/info` | 查询详情 | `UserController` | [getUserInfo](../interfaces/get-user-info-getuserinfo.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/user/list` | 查询列表 | `UserController` | [getUserList](../interfaces/get-user-list-getuserlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/user/page` | 分页查询 | `UserController` | [getUserPage](../interfaces/get-user-page-getuserpage.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/user/update` | POST /user/update | `UserController` | [updateUser](../interfaces/post-user-update-updateuser.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
