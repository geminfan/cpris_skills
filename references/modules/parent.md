# parent 模块 REST 接口

共 55 个已识别接口。

## 接口列表

| 方法 | 路径 | 功能 | Controller | 详情 |
|---|---|---|---|---|
| GET | `/parent/assess/list` | 查询列表 | `ParentAssessController` | [getAssessList](../interfaces/get-parent-assess-list-getassesslist.md) |
| GET | `/parent/assess/result/info` | 查询详情 | `ParentAssessController` | [getAssessResultInfo](../interfaces/get-parent-assess-result-info-getassessresultinfo.md) |
| POST | `/parent/assess/result/saveOrUpdate` | 新增或更新 | `ParentAssessController` | [saveOrUpdateAssessResult](../interfaces/post-parent-assess-result-saveorupdate-saveorupdateassessresult.md) |
| GET | `/parent/assess/result/status/map` | GET /parent/assess/result/status/map | `ParentAssessController` | [getAssessPaperResultStatus](../interfaces/get-parent-assess-result-status-map-getassesspaperresultstatus.md) |
| GET | `/parent/assessDefine/paper/list` | 查询列表 | `ParentAssessDefineController` | [getAssessDefinePaperList](../interfaces/get-parent-assessdefine-paper-list-getassessdefinepaperlist.md) |
| GET | `/parent/children/behavior/info` | 查询详情 | `ParentChildrenController` | [getChildrenRegBehavior](../interfaces/get-parent-children-behavior-info-getchildrenregbehavior.md) |
| POST | `/parent/children/behavior/saveOrUpdate` | 新增或更新 | `ParentChildrenController` | [saveOrUpdateChildrenRegBehavior](../interfaces/post-parent-children-behavior-saveorupdate-saveorupdatechildrenregbehavior.md) |
| GET | `/parent/children/common/info` | 查询详情 | `ParentChildrenController` | [getChildrenCommonInfo](../interfaces/get-parent-children-common-info-getchildrencommoninfo.md) |
| GET | `/parent/children/growth/info` | 查询详情 | `ParentChildrenController` | [getChildrenRegGrowth](../interfaces/get-parent-children-growth-info-getchildrenreggrowth.md) |
| POST | `/parent/children/growth/saveOrUpdate` | 新增或更新 | `ParentChildrenController` | [saveOrUpdateChildrenRegGrowth](../interfaces/post-parent-children-growth-saveorupdate-saveorupdatechildrenreggrowth.md) |
| GET | `/parent/children/guardian/list` | 查询列表 | `ParentChildrenController` | [getChildrenGuardianList](../interfaces/get-parent-children-guardian-list-getchildrenguardianlist.md) |
| POST | `/parent/children/guardian/saveOrUpdate` | 查询列表 | `ParentChildrenController` | [saveOrUpdateChildrenGuardianList](../interfaces/post-parent-children-guardian-saveorupdate-saveorupdatechildrenguardianlist.md) |
| GET | `/parent/children/history/record/info` | 查询详情 | `ParentChildrenController` | [getChildrenHistoryRecord](../interfaces/get-parent-children-history-record-info-getchildrenhistoryrecord.md) |
| POST | `/parent/children/history/record/saveOrUpdate` | 新增或更新 | `ParentChildrenController` | [saveOrUpdateChildrenHistoryRecord](../interfaces/post-parent-children-history-record-saveorupdate-saveorupdatechildrenhistoryrecord.md) |
| GET | `/parent/children/image/list` | 查询列表 | `ParentChildrenController` | [getChildrenImageList](../interfaces/get-parent-children-image-list-getchildrenimagelist.md) |
| POST | `/parent/children/image/saveOrUpdate` | 查询列表 | `ParentChildrenController` | [saveOrUpdateChildrenImageList](../interfaces/post-parent-children-image-saveorupdate-saveorupdatechildrenimagelist.md) |
| GET | `/parent/children/info` | 查询详情 | `ParentChildrenController` | [getChildrenInfo](../interfaces/get-parent-children-info-getchildreninfo.md) |
| GET | `/parent/children/list` | 查询列表 | `ParentChildrenController` | [getChildList](../interfaces/get-parent-children-list-getchildlist.md) |
| POST | `/parent/children/saveOrUpdate` | 查询详情 | `ParentChildrenController` | [saveOrUpdateChildrenInfo](../interfaces/post-parent-children-saveorupdate-saveorupdatechildreninfo.md) |
| GET | `/parent/children/visit/info` | 查询详情 | `ParentChildrenController` | [getChildrenVisit](../interfaces/get-parent-children-visit-info-getchildrenvisit.md) |
| POST | `/parent/children/visit/saveOrUpdate` | 新增或更新 | `ParentChildrenController` | [saveOrUpdateChildrenVisit](../interfaces/post-parent-children-visit-saveorupdate-saveorupdatechildrenvisit.md) |
| GET | `/parent/periodical/item/list` | 查询列表 | `ParentPeriodicalController` | [getPeriodicalItemList](../interfaces/get-parent-periodical-item-list-getperiodicalitemlist.md) |
| POST | `/parent/periodical/plan/delete` | 删除 | `ParentPeriodicalController` | [deletePeriodicalPlan](../interfaces/post-parent-periodical-plan-delete-deleteperiodicalplan.md) |
| GET | `/parent/periodical/plan/info` | 查询详情 | `ParentPeriodicalController` | [getPeriodicalPlanInfo](../interfaces/get-parent-periodical-plan-info-getperiodicalplaninfo.md) |
| GET | `/parent/periodical/plan/list` | 查询列表 | `ParentPeriodicalController` | [getPeriodicalList](../interfaces/get-parent-periodical-plan-list-getperiodicallist.md) |
| GET | `/parent/periodical/plan/page` | 分页查询 | `ParentPeriodicalController` | [getPeriodicalPage](../interfaces/get-parent-periodical-plan-page-getperiodicalpage.md) |
| POST | `/parent/periodical/plan/saveOrUpdate` | 新增或更新 | `ParentPeriodicalController` | [periodicalPlanSaveOrUpdate](../interfaces/post-parent-periodical-plan-saveorupdate-periodicalplansaveorupdate.md) |
| POST | `/parent/periodical/plan/subGuideItem/list` | 查询列表 | `ParentPeriodicalController` | [getPlanSubGuideItemList](../interfaces/post-parent-periodical-plan-subguideitem-list-getplansubguideitemlist.md) |
| GET | `/parent/periodical/recent/item/List` | 查询列表 | `ParentPeriodicalController` | [getRecentPeriodicalItemList](../interfaces/get-parent-periodical-recent-item-list-getrecentperiodicalitemlist.md) |
| GET | `/parent/periodical/record/list` | 查询列表 | `ParentPeriodicalController` | [getRecordList](../interfaces/get-parent-periodical-record-list-getrecordlist.md) |
| POST | `/parent/periodical/record/saveOrUpdate` | 新增或更新 | `ParentPeriodicalController` | [recordSaveOrUpdate](../interfaces/post-parent-periodical-record-saveorupdate-recordsaveorupdate.md) |
| GET | `/parent/periodical/record/type/list` | 查询列表 | `ParentPeriodicalController` | [getTrainingRecordList](../interfaces/get-parent-periodical-record-type-list-gettrainingrecordlist.md) |
| POST | `/parent/periodical/signature/saveOrUpdate` | 新增或更新 | `ParentPeriodicalController` | [saveOrUpdateSignature](../interfaces/post-parent-periodical-signature-saveorupdate-saveorupdatesignature.md) |
| GET | `/parent/team/child/enter/list` | 查询列表 | `ParentTeamController` | [getTeamEnterList](../interfaces/get-parent-team-child-enter-list-getteamenterlist.md) |
| GET | `/parent/team/count` | 查询详情 | `ParentTeamController` | [getChildrenInfoCount](../interfaces/get-parent-team-count-getchildreninfocount.md) |
| POST | `/parent/team/lesson/delete` | 删除 | `ParentTeamController` | [deleteTeamLesson](../interfaces/post-parent-team-lesson-delete-deleteteamlesson.md) |
| GET | `/parent/team/lesson/info` | 查询详情 | `ParentTeamController` | [getTeamLessonInfo](../interfaces/get-parent-team-lesson-info-getteamlessoninfo.md) |
| POST | `/parent/team/lesson/onlyOne/delete` | 删除 | `ParentTeamController` | [deleteOnlyOneTeamLesson](../interfaces/post-parent-team-lesson-onlyone-delete-deleteonlyoneteamlesson.md) |
| POST | `/parent/team/lesson/saveOrUpdate` | 新增或更新 | `ParentTeamController` | [saveOrUpdateTeamLesson](../interfaces/post-parent-team-lesson-saveorupdate-saveorupdateteamlesson.md) |
| GET | `/parent/team/lesson/summarized/list` | 查询列表 | `ParentTeamController` | [getTrainingList](../interfaces/get-parent-team-lesson-summarized-list-gettraininglist.md) |
| GET | `/parent/team/lesson/summary/info` | 查询详情 | `ParentTeamController` | [getLessonSummaryInfo](../interfaces/get-parent-team-lesson-summary-info-getlessonsummaryinfo.md) |
| POST | `/parent/team/lesson/summary/saveOrUpdate` | 新增或更新 | `ParentTeamController` | [saveOrUpdateLessonSummary](../interfaces/post-parent-team-lesson-summary-saveorupdate-saveorupdatelessonsummary.md) |
| GET | `/parent/team/lesson/summary/type/list` | 查询列表 | `ParentTeamController` | [getTeamSummaryTypeList](../interfaces/get-parent-team-lesson-summary-type-list-getteamsummarytypelist.md) |
| POST | `/parent/team/list` | 查询列表 | `ParentTeamController` | [getTeamList](../interfaces/post-parent-team-list-getteamlist.md) |
| POST | `/parent/team/scheme/all/list` | 查询列表 | `ParentTeamController` | [getAllTeamSchemeList](../interfaces/post-parent-team-scheme-all-list-getallteamschemelist.md) |
| POST | `/parent/team/scheme/all/page` | 分页查询 | `ParentTeamController` | [getAllTeamSchemePage](../interfaces/post-parent-team-scheme-all-page-getallteamschemepage.md) |
| POST | `/parent/team/scheme/common/list` | 查询列表 | `ParentTeamController` | [getTeamSchemeCommonList](../interfaces/post-parent-team-scheme-common-list-getteamschemecommonlist.md) |
| POST | `/parent/team/scheme/common/page` | 分页查询 | `ParentTeamController` | [getTeamSchemeCommonPage](../interfaces/post-parent-team-scheme-common-page-getteamschemecommonpage.md) |
| GET | `/parent/team/scheme/info` | 查询详情 | `ParentTeamController` | [getSchemeInfo](../interfaces/get-parent-team-scheme-info-getschemeinfo.md) |
| GET | `/parent/team/scheme/level/map` | GET /parent/team/scheme/level/map | `ParentTeamController` | [getSchemeLevelMap](../interfaces/get-parent-team-scheme-level-map-getschemelevelmap.md) |
| POST | `/parent/team/scheme/list` | 查询列表 | `ParentTeamController` | [getTeamSchemeList](../interfaces/post-parent-team-scheme-list-getteamschemelist.md) |
| POST | `/parent/team/scheme/page` | 分页查询 | `ParentTeamController` | [getTeamSchemePage](../interfaces/post-parent-team-scheme-page-getteamschemepage.md) |
| POST | `/parent/team/scheme/step/list` | 查询列表 | `ParentTeamController` | [getSchemeStepList](../interfaces/post-parent-team-scheme-step-list-getschemesteplist.md) |
| GET | `/parent/team/scheme/type/list` | 查询列表 | `ParentTeamController` | [getTeamCourseSchemeTypeList](../interfaces/get-parent-team-scheme-type-list-getteamcourseschemetypelist.md) |
| POST | `/parent/team/signature/saveOrUpdate` | 新增或更新 | `ParentTeamController` | [saveOrUpdateSignature](../interfaces/post-parent-team-signature-saveorupdate-saveorupdatesignature.md) |
