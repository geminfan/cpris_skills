# training 模块 REST 接口

共 42 个已识别接口。

## 接口列表

| 方法 | 路径 | 功能 | Controller | 详情 |
|---|---|---|---|---|
| POST | `/iepLib/more/saveOrUpdate` | 查询列表 | `IepLibController` | [saveOrUpdateIepLibList](../interfaces/post-ieplib-more-saveorupdate-saveorupdateiepliblist.md) |
| POST | `/iepLib/myIep/list` | 查询列表 | `IepLibController` | [getMyIepLibList](../interfaces/post-ieplib-myiep-list-getmyiepliblist.md) |
| POST | `/iepLib/myIep/page` | 分页查询 | `IepLibController` | [getMyIepLibPage](../interfaces/post-ieplib-myiep-page-getmyieplibpage.md) |
| POST | `/iepLib/publicIep/list` | 查询列表 | `IepLibController` | [getPublicIepLibList](../interfaces/post-ieplib-publiciep-list-getpubliciepliblist.md) |
| POST | `/iepLib/publicIep/page` | 分页查询 | `IepLibController` | [getPublicIepLibPage](../interfaces/post-ieplib-publiciep-page-getpublicieplibpage.md) |
| POST | `/iepLib/saveOrUpdate` | 新增或更新 | `IepLibController` | [saveOrUpdateIepLib](../interfaces/post-ieplib-saveorupdate-saveorupdateieplib.md) |
| GET | `/periodical/item/list` | 查询列表 | `PeriodicalController` | [getPeriodicalItemList](../interfaces/get-periodical-item-list-getperiodicalitemlist.md) |
| POST | `/periodical/plan/delete` | 删除 | `PeriodicalController` | [deletePeriodicalPlan](../interfaces/post-periodical-plan-delete-deleteperiodicalplan.md) |
| GET | `/periodical/plan/info` | 查询详情 | `PeriodicalController` | [getPeriodicalPlanInfo](../interfaces/get-periodical-plan-info-getperiodicalplaninfo.md) |
| POST | `/periodical/plan/saveOrUpdate` | 新增或更新 | `PeriodicalController` | [periodicalPlanSaveOrUpdate](../interfaces/post-periodical-plan-saveorupdate-periodicalplansaveorupdate.md) |
| POST | `/periodical/plan/subGuideItem/list` | 查询列表 | `PeriodicalController` | [getPlanSubGuideItemList](../interfaces/post-periodical-plan-subguideitem-list-getplansubguideitemlist.md) |
| GET | `/periodical/recent/item/List` | 查询列表 | `PeriodicalController` | [getRecentPeriodicalItemList](../interfaces/get-periodical-recent-item-list-getrecentperiodicalitemlist.md) |
| GET | `/periodical/record/list` | 查询列表 | `PeriodicalController` | [getRecordList](../interfaces/get-periodical-record-list-getrecordlist.md) |
| POST | `/periodical/record/saveOrUpdate` | 新增或更新 | `PeriodicalController` | [recordSaveOrUpdate](../interfaces/post-periodical-record-saveorupdate-recordsaveorupdate.md) |
| GET | `/periodical/record/type/list` | 查询列表 | `PeriodicalController` | [getTrainingRecordList](../interfaces/get-periodical-record-type-list-gettrainingrecordlist.md) |
| GET | `/periodical/year/list` | 查询列表 | `PeriodicalController` | [getPeriodicalPlanYearList](../interfaces/get-periodical-year-list-getperiodicalplanyearlist.md) |
| GET | `/periodical/year/page` | 分页查询 | `PeriodicalController` | [getPeriodicalPlanYearPage](../interfaces/get-periodical-year-page-getperiodicalplanyearpage.md) |
| GET | `/team/child/enter/list` | 查询列表 | `TeamController` | [getTeamEnterList](../interfaces/get-team-child-enter-list-getteamenterlist.md) |
| GET | `/team/count` | 查询详情 | `TeamController` | [getChildrenInfoCount](../interfaces/get-team-count-getchildreninfocount.md) |
| GET | `/team/dateRange/list` | 查询列表 | `TeamController` | [getLessonDateRangeList](../interfaces/get-team-daterange-list-getlessondaterangelist.md) |
| GET | `/team/dateRange/page` | 分页查询 | `TeamController` | [getLessonDateRangePage](../interfaces/get-team-daterange-page-getlessondaterangepage.md) |
| POST | `/team/lesson/delete` | 删除 | `TeamController` | [deleteTeamLesson](../interfaces/post-team-lesson-delete-deleteteamlesson.md) |
| GET | `/team/lesson/info` | 查询详情 | `TeamController` | [getTeamLessonInfo](../interfaces/get-team-lesson-info-getteamlessoninfo.md) |
| POST | `/team/lesson/onlyOne/delete` | 删除 | `TeamController` | [deleteOnlyOneTeamLesson](../interfaces/post-team-lesson-onlyone-delete-deleteonlyoneteamlesson.md) |
| POST | `/team/lesson/saveOrUpdate` | 新增或更新 | `TeamController` | [saveOrUpdateTeamLesson](../interfaces/post-team-lesson-saveorupdate-saveorupdateteamlesson.md) |
| GET | `/team/lesson/summary/info` | 查询详情 | `TeamController` | [getLessonSummaryInfo](../interfaces/get-team-lesson-summary-info-getlessonsummaryinfo.md) |
| POST | `/team/lesson/summary/saveOrUpdate` | 新增或更新 | `TeamController` | [saveOrUpdateLessonSummary](../interfaces/post-team-lesson-summary-saveorupdate-saveorupdatelessonsummary.md) |
| GET | `/team/lesson/summary/type/list` | 查询列表 | `TeamController` | [getTeamSummaryTypeList](../interfaces/get-team-lesson-summary-type-list-getteamsummarytypelist.md) |
| POST | `/team/list` | 查询列表 | `TeamController` | [getTeamList](../interfaces/post-team-list-getteamlist.md) |
| POST | `/team/scheme/all/list` | 查询列表 | `TeamController` | [getAllTeamSchemeList](../interfaces/post-team-scheme-all-list-getallteamschemelist.md) |
| POST | `/team/scheme/all/page` | 分页查询 | `TeamController` | [getAllTeamSchemePage](../interfaces/post-team-scheme-all-page-getallteamschemepage.md) |
| POST | `/team/scheme/common/list` | 查询列表 | `TeamController` | [getTeamSchemeCommonList](../interfaces/post-team-scheme-common-list-getteamschemecommonlist.md) |
| POST | `/team/scheme/common/page` | 分页查询 | `TeamController` | [getTeamSchemeCommonPage](../interfaces/post-team-scheme-common-page-getteamschemecommonpage.md) |
| GET | `/team/scheme/info` | 查询详情 | `TeamController` | [getSchemeInfo](../interfaces/get-team-scheme-info-getschemeinfo.md) |
| GET | `/team/scheme/level/map` | GET /team/scheme/level/map | `TeamController` | [getSchemeLevelMap](../interfaces/get-team-scheme-level-map-getschemelevelmap.md) |
| POST | `/team/scheme/list` | 查询列表 | `TeamController` | [getTeamSchemeList](../interfaces/post-team-scheme-list-getteamschemelist.md) |
| POST | `/team/scheme/page` | 分页查询 | `TeamController` | [getTeamSchemePage](../interfaces/post-team-scheme-page-getteamschemepage.md) |
| POST | `/team/scheme/step/list` | 查询列表 | `TeamController` | [getSchemeStepList](../interfaces/post-team-scheme-step-list-getschemesteplist.md) |
| GET | `/team/scheme/type/list` | 查询列表 | `TeamController` | [getTeamCourseSchemeTypeList](../interfaces/get-team-scheme-type-list-getteamcourseschemetypelist.md) |
| GET | `/training/dateRange/count` | 统计数量 | `TrainingController` | [getDateRangeCount](../interfaces/get-training-daterange-count-getdaterangecount.md) |
| GET | `/training/list` | 查询列表 | `TrainingController` | [getTrainingList](../interfaces/get-training-list-gettraininglist.md) |
| GET | `/training/today/count` | 统计数量 | `TrainingController` | [getTrainingCount](../interfaces/get-training-today-count-gettrainingcount.md) |
