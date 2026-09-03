# assess 模块 REST 接口

共 37 个已识别接口。

本模块为静态接口资料；调用资格见表末列，具体约束见 [网关契约](../gateway-contract.md)。

## 接口列表

| 方法 | 路径 | 功能 | Controller | 详情  AI 调用 |
|---|---|---|---|---|---|
| POST | `/assess/delete` | 删除 | `AssessController` | [deleteAssess](../interfaces/post-assess-delete-deleteassess.md)  禁止调用：网关删除禁令 |
| POST | `/assess/finish` | 完成 | `AssessController` | [finishAssess](../interfaces/post-assess-finish-finishassess.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assess/info` | 查询详情 | `AssessController` | [getAssessInfo](../interfaces/get-assess-info-getassessinfo.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assess/list` | 查询列表 | `AssessController` | [getAssessList](../interfaces/get-assess-list-getassesslist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assess/page` | 分页查询 | `AssessController` | [getAssessPage](../interfaces/get-assess-page-getassesspage.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/assess/report/generate` | 生成 | `AssessController` | [generateReportPdf](../interfaces/post-assess-report-generate-generatereportpdf.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assess/report/info` | 查询详情 | `AssessController` | [getAssessReport](../interfaces/get-assess-report-info-getassessreport.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/assess/report/summary/generate` | 生成 | `AssessController` | [generateReportSummary](../interfaces/post-assess-report-summary-generate-generatereportsummary.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assess/report/summary/info` | 查询详情 | `AssessController` | [getAssessReportSummaryInfo](../interfaces/get-assess-report-summary-info-getassessreportsummaryinfo.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/assess/report/summary/update` | POST /assess/report/summary/update | `AssessController` | [updateReportSummary](../interfaces/post-assess-report-summary-update-updatereportsummary.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/assess/result/delete` | 删除 | `AssessController` | [deleteAssessResult](../interfaces/post-assess-result-delete-deleteassessresult.md)  禁止调用：网关删除禁令 |
| POST | `/assess/result/generate` | 生成 | `AssessController` | [generateAssessResult](../interfaces/post-assess-result-generate-generateassessresult.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assess/result/info` | 查询详情 | `AssessController` | [getAssessResultInfo](../interfaces/get-assess-result-info-getassessresultinfo.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assess/result/item/info` | 查询详情 | `AssessController` | [getAssessItemResult](../interfaces/get-assess-result-item-info-getassessitemresult.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/assess/result/item/saveOrUpdate` | 新增或更新 | `AssessController` | [saveOrUpdateAssessItemResult](../interfaces/post-assess-result-item-saveorupdate-saveorupdateassessitemresult.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assess/result/list` | 查询列表 | `AssessController` | [getAssessResultList](../interfaces/get-assess-result-list-getassessresultlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/assess/result/saveOrUpdate` | 新增或更新 | `AssessController` | [saveOrUpdateAssessResult](../interfaces/post-assess-result-saveorupdate-saveorupdateassessresult.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assess/result/status/map` | GET /assess/result/status/map | `AssessController` | [getAssessPaperResultStatus](../interfaces/get-assess-result-status-map-getassesspaperresultstatus.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/assess/saveOrUpdate` | 新增或更新 | `AssessController` | [saveOrUpdateAssess](../interfaces/post-assess-saveorupdate-saveorupdateassess.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/assess/unFinish` | 完成 | `AssessController` | [unFinishAssess](../interfaces/post-assess-unfinish-unfinishassess.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assessDefine/andOther/list` | 查询列表 | `AssessDefineController` | [getAssessDefineList2](../interfaces/get-assessdefine-andother-list-getassessdefinelist2.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assessDefine/items/list` | 查询列表 | `AssessDefineController` | [getAssessDefineItemsList](../interfaces/get-assessdefine-items-list-getassessdefineitemslist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assessDefine/list` | 查询列表 | `AssessDefineController` | [getAssessDefineList](../interfaces/get-assessdefine-list-getassessdefinelist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assessDefine/page` | 分页查询 | `AssessDefineController` | [getAssessDefinePage](../interfaces/get-assessdefine-page-getassessdefinepage.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assessDefine/paper/list` | 查询列表 | `AssessDefineController` | [getAssessDefinePaperList](../interfaces/get-assessdefine-paper-list-getassessdefinepaperlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assessDefine/type/count` | 统计数量 | `AssessDefineController` | [getAssessDefineTypeCount](../interfaces/get-assessdefine-type-count-getassessdefinetypecount.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assessDefine/type/map` | GET /assessDefine/type/map | `AssessDefineController` | [getAssessTypeMap](../interfaces/get-assessdefine-type-map-getassesstypemap.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/assessGuide/generate` | 生成 | `AssessGuideController` | [generateAssessGuide](../interfaces/post-assessguide-generate-generateassessguide.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/assessGuide/parent/guide/list` | 查询列表 | `AssessGuideController` | [getParentGuideList](../interfaces/post-assessguide-parent-guide-list-getparentguidelist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/assessGuide/teacher/guide/list` | 查询列表 | `AssessGuideController` | [getTeacherGuideList](../interfaces/post-assessguide-teacher-guide-list-getteacherguidelist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assess/cars/question/list` | 查询列表 | `CarsController` | [getAssessDefineCarsQuestionList](../interfaces/get-assess-cars-question-list-getassessdefinecarsquestionlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/assess/cars/result/saveOrUpdate` | 新增或更新 | `CarsController` | [saveOrUpdateAssessCarsResult](../interfaces/post-assess-cars-result-saveorupdate-saveorupdateassesscarsresult.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assess/cars/result/status/map` | GET /assess/cars/result/status/map | `CarsController` | [getCarsPaperResultStatus](../interfaces/get-assess-cars-result-status-map-getcarspaperresultstatus.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assess/mte1/parent/question/list` | 查询列表 | `Mte1Controller` | [getMte1ParentQuestionList](../interfaces/get-assess-mte1-parent-question-list-getmte1parentquestionlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| POST | `/assess/mte1/result/saveOrUpdate` | 新增或更新 | `Mte1Controller` | [saveOrUpdateTeacherResult](../interfaces/post-assess-mte1-result-saveorupdate-saveorupdateteacherresult.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assess/mte1/result/status/map` | GET /assess/mte1/result/status/map | `Mte1Controller` | [getMte1PaperResultStatus](../interfaces/get-assess-mte1-result-status-map-getmte1paperresultstatus.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
| GET | `/assess/mte1/teacher/question/list` | 查询列表 | `Mte1Controller` | [getMte1TeacherQuestionList](../interfaces/get-assess-mte1-teacher-question-list-getmte1teacherquestionlist.md)  经 AI 网关调用，受用户授权与运行时权限约束 |
