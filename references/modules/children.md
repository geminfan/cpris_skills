# children 模块 REST 接口

共 20 个已识别接口。

本模块为静态接口资料；调用资格见表末列，具体约束见 [网关契约](../gateway-contract.md)。

## 接口列表

| 方法 | 路径 | 功能 | Controller | 详情  AI 调用 |
|---|---|---|---|---|---|
| POST | `/childrenInfo/behavior/saveOrUpdate` | 查询详情 | `ChildrenInfoController` | [getChildrenRegBehavior](../interfaces/post-childreninfo-behavior-saveorupdate-getchildrenregbehavior.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/childrenInfo/checkName` | 查询详情 | `ChildrenInfoController` | [checkChildName](../interfaces/get-childreninfo-checkname-checkchildname.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/childrenInfo/common/info` | 查询详情 | `ChildrenInfoController` | [getChildrenCommonInfo](../interfaces/get-childreninfo-common-info-getchildrencommoninfo.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/childrenInfo/count` | 查询详情 | `ChildrenInfoController` | [getChildrenInfoCount](../interfaces/get-childreninfo-count-getchildreninfocount.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/childrenInfo/delete` | 查询详情 | `ChildrenInfoController` | [deleteChildrenInfo](../interfaces/post-childreninfo-delete-deletechildreninfo.md)  禁止调用：网关删除禁令 |
| POST | `/childrenInfo/enterTraining` | 查询详情 | `ChildrenInfoController` | [childEnterTraining](../interfaces/post-childreninfo-entertraining-childentertraining.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/childrenInfo/enterTraining/info` | 查询详情 | `ChildrenInfoController` | [childEnterTrainingInfo](../interfaces/get-childreninfo-entertraining-info-childentertraininginfo.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/childrenInfo/growth/saveOrUpdate` | 查询详情 | `ChildrenInfoController` | [saveOrUpdateChildrenRegGrowth](../interfaces/post-childreninfo-growth-saveorupdate-saveorupdatechildrenreggrowth.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/childrenInfo/guardian/saveOrUpdate` | 查询列表 | `ChildrenInfoController` | [saveOrUpdateChildrenGuardianList](../interfaces/post-childreninfo-guardian-saveorupdate-saveorupdatechildrenguardianlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/childrenInfo/history/record/saveOrUpdate` | 查询详情 | `ChildrenInfoController` | [saveOrUpdateChildrenHistoryRecord](../interfaces/post-childreninfo-history-record-saveorupdate-saveorupdatechildrenhistoryrecord.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/childrenInfo/image/saveOrUpdate` | 查询列表 | `ChildrenInfoController` | [saveOrUpdateChildrenImageList](../interfaces/post-childreninfo-image-saveorupdate-saveorupdatechildrenimagelist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/childrenInfo/info` | 查询详情 | `ChildrenInfoController` | [getChildrenInfo](../interfaces/get-childreninfo-info-getchildreninfo.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/childrenInfo/list` | 查询列表 | `ChildrenInfoController` | [getChildrenInfoList](../interfaces/post-childreninfo-list-getchildreninfolist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/childrenInfo/nation/list` | 查询列表 | `ChildrenInfoController` | [getNationList](../interfaces/get-childreninfo-nation-list-getnationlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/childrenInfo/page` | 分页查询 | `ChildrenInfoController` | [getChildrenInfoPage](../interfaces/get-childreninfo-page-getchildreninfopage.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/childrenInfo/region/list` | 查询列表 | `ChildrenInfoController` | [getRegionList](../interfaces/get-childreninfo-region-list-getregionlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/childrenInfo/rxlb/get` | 查询详情 | `ChildrenInfoController` | [getRxlb](../interfaces/get-childreninfo-rxlb-get-getrxlb.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/childrenInfo/saveOrUpdate` | 查询详情 | `ChildrenInfoController` | [saveOrUpdateChildrenInfo](../interfaces/post-childreninfo-saveorupdate-saveorupdatechildreninfo.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/childrenInfo/visit/saveOrUpdate` | 查询详情 | `ChildrenInfoController` | [saveOrUpdateChildrenVisit](../interfaces/post-childreninfo-visit-saveorupdate-saveorupdatechildrenvisit.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/childrenInfo/zdmc/list` | 查询列表 | `ChildrenInfoController` | [getZdmcList](../interfaces/get-childreninfo-zdmc-list-getzdmclist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
