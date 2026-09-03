# training 模块 REST 接口

共 42 个已识别接口。

本模块为静态接口资料；调用资格见表末列，具体约束见 [网关契约](../gateway-contract.md)。

## 接口列表

| 方法 | 路径 | 功能 | Controller | 详情  AI 调用 |
|---|---|---|---|---|---|
| POST | `/iepLib/more/saveOrUpdate` | 查询列表 | `IepLibController` | [saveOrUpdateIepLibList](../interfaces/post-ieplib-more-saveorupdate-saveorupdateiepliblist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/iepLib/myIep/list` | 查询列表 | `IepLibController` | [getMyIepLibList](../interfaces/post-ieplib-myiep-list-getmyiepliblist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/iepLib/myIep/page` | 分页查询 | `IepLibController` | [getMyIepLibPage](../interfaces/post-ieplib-myiep-page-getmyieplibpage.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/iepLib/publicIep/list` | 查询列表 | `IepLibController` | [getPublicIepLibList](../interfaces/post-ieplib-publiciep-list-getpubliciepliblist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/iepLib/publicIep/page` | 分页查询 | `IepLibController` | [getPublicIepLibPage](../interfaces/post-ieplib-publiciep-page-getpublicieplibpage.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/iepLib/saveOrUpdate` | 新增或更新 | `IepLibController` | [saveOrUpdateIepLib](../interfaces/post-ieplib-saveorupdate-saveorupdateieplib.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/periodical/item/list` | 查询列表 | `PeriodicalController` | [getPeriodicalItemList](../interfaces/get-periodical-item-list-getperiodicalitemlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/periodical/plan/delete` | 删除 | `PeriodicalController` | [deletePeriodicalPlan](../interfaces/post-periodical-plan-delete-deleteperiodicalplan.md)  禁止调用：网关删除禁令 |
| GET | `/periodical/plan/info` | 查询详情 | `PeriodicalController` | [getPeriodicalPlanInfo](../interfaces/get-periodical-plan-info-getperiodicalplaninfo.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/periodical/plan/saveOrUpdate` | 新增或更新 | `PeriodicalController` | [periodicalPlanSaveOrUpdate](../interfaces/post-periodical-plan-saveorupdate-periodicalplansaveorupdate.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/periodical/plan/subGuideItem/list` | 查询列表 | `PeriodicalController` | [getPlanSubGuideItemList](../interfaces/post-periodical-plan-subguideitem-list-getplansubguideitemlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/periodical/recent/item/List` | 查询列表 | `PeriodicalController` | [getRecentPeriodicalItemList](../interfaces/get-periodical-recent-item-list-getrecentperiodicalitemlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/periodical/record/list` | 查询列表 | `PeriodicalController` | [getRecordList](../interfaces/get-periodical-record-list-getrecordlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/periodical/record/saveOrUpdate` | 新增或更新 | `PeriodicalController` | [recordSaveOrUpdate](../interfaces/post-periodical-record-saveorupdate-recordsaveorupdate.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/periodical/record/type/list` | 查询列表 | `PeriodicalController` | [getTrainingRecordList](../interfaces/get-periodical-record-type-list-gettrainingrecordlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/periodical/year/list` | 查询列表 | `PeriodicalController` | [getPeriodicalPlanYearList](../interfaces/get-periodical-year-list-getperiodicalplanyearlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/periodical/year/page` | 分页查询 | `PeriodicalController` | [getPeriodicalPlanYearPage](../interfaces/get-periodical-year-page-getperiodicalplanyearpage.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/team/child/enter/list` | 查询列表 | `TeamController` | [getTeamEnterList](../interfaces/get-team-child-enter-list-getteamenterlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/team/count` | 查询详情 | `TeamController` | [getChildrenInfoCount](../interfaces/get-team-count-getchildreninfocount.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/team/dateRange/list` | 查询列表 | `TeamController` | [getLessonDateRangeList](../interfaces/get-team-daterange-list-getlessondaterangelist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/team/dateRange/page` | 分页查询 | `TeamController` | [getLessonDateRangePage](../interfaces/get-team-daterange-page-getlessondaterangepage.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/team/lesson/delete` | 删除 | `TeamController` | [deleteTeamLesson](../interfaces/post-team-lesson-delete-deleteteamlesson.md)  禁止调用：网关删除禁令 |
| GET | `/team/lesson/info` | 查询详情 | `TeamController` | [getTeamLessonInfo](../interfaces/get-team-lesson-info-getteamlessoninfo.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/team/lesson/onlyOne/delete` | 删除 | `TeamController` | [deleteOnlyOneTeamLesson](../interfaces/post-team-lesson-onlyone-delete-deleteonlyoneteamlesson.md)  禁止调用：网关删除禁令 |
| POST | `/team/lesson/saveOrUpdate` | 新增或更新 | `TeamController` | [saveOrUpdateTeamLesson](../interfaces/post-team-lesson-saveorupdate-saveorupdateteamlesson.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/team/lesson/summary/info` | 查询详情 | `TeamController` | [getLessonSummaryInfo](../interfaces/get-team-lesson-summary-info-getlessonsummaryinfo.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/team/lesson/summary/saveOrUpdate` | 新增或更新 | `TeamController` | [saveOrUpdateLessonSummary](../interfaces/post-team-lesson-summary-saveorupdate-saveorupdatelessonsummary.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/team/lesson/summary/type/list` | 查询列表 | `TeamController` | [getTeamSummaryTypeList](../interfaces/get-team-lesson-summary-type-list-getteamsummarytypelist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/team/list` | 查询列表 | `TeamController` | [getTeamList](../interfaces/post-team-list-getteamlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/team/scheme/all/list` | 查询列表 | `TeamController` | [getAllTeamSchemeList](../interfaces/post-team-scheme-all-list-getallteamschemelist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/team/scheme/all/page` | 分页查询 | `TeamController` | [getAllTeamSchemePage](../interfaces/post-team-scheme-all-page-getallteamschemepage.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/team/scheme/common/list` | 查询列表 | `TeamController` | [getTeamSchemeCommonList](../interfaces/post-team-scheme-common-list-getteamschemecommonlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/team/scheme/common/page` | 分页查询 | `TeamController` | [getTeamSchemeCommonPage](../interfaces/post-team-scheme-common-page-getteamschemecommonpage.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/team/scheme/info` | 查询详情 | `TeamController` | [getSchemeInfo](../interfaces/get-team-scheme-info-getschemeinfo.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/team/scheme/level/map` | GET /team/scheme/level/map | `TeamController` | [getSchemeLevelMap](../interfaces/get-team-scheme-level-map-getschemelevelmap.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/team/scheme/list` | 查询列表 | `TeamController` | [getTeamSchemeList](../interfaces/post-team-scheme-list-getteamschemelist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/team/scheme/page` | 分页查询 | `TeamController` | [getTeamSchemePage](../interfaces/post-team-scheme-page-getteamschemepage.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/team/scheme/step/list` | 查询列表 | `TeamController` | [getSchemeStepList](../interfaces/post-team-scheme-step-list-getschemesteplist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/team/scheme/type/list` | 查询列表 | `TeamController` | [getTeamCourseSchemeTypeList](../interfaces/get-team-scheme-type-list-getteamcourseschemetypelist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/training/dateRange/count` | 统计数量 | `TrainingController` | [getDateRangeCount](../interfaces/get-training-daterange-count-getdaterangecount.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/training/list` | 查询列表 | `TrainingController` | [getTrainingList](../interfaces/get-training-list-gettraininglist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/training/today/count` | 统计数量 | `TrainingController` | [getTrainingCount](../interfaces/get-training-today-count-gettrainingcount.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
