# CPRIS 微信端 REST API 总览

原静态快照包含 **179** 项 Controller 映射。下表是收录文档数，包含不可调用的 SaaS 和删除接口，不代表当前部署的可调用接口数量。

路径为 {aiGateway}/ai/gw/{service}/{业务路径}。默认测试 http://testai.cpris.com，正式 https://aiskills.cpris.com 需显式选择。仅使用 X-Api-Key，业务网关由服务端访问。

| 模块 | 文档接口数 | service | 范围 |
|---|---:|---|---|
| [assess](modules/assess.md) | 37 | assess | 评估，删除接口禁止 |
| [children](modules/children.md) | 20 | children | 儿童/监护人，删除接口禁止 |
| [parent](modules/parent.md) | 55 | parent | 家长业务，删除接口禁止 |
| [saas](modules/saas.md) | 20 | 无 | 仅源码参考，不供技能调用 |
| [training](modules/training.md) | 42 | training | 训练/团队/计划，删除接口禁止 |
| [user](modules/user.md) | 5 | user | 用户信息，头像上传需要 multipart 调用方 |

merchant 已配置后端路由，但快照没有接口资料；不能仅凭存在路由猜测具体接口。

## 阅读方式

1. 按业务选择模块，查看“AI 调用”列，再阅读接口详情。
2. 从完整方法签名和参数分组确定请求；有源码时沿 cpris_wxapp/ 相对路径追踪。
3. 按 [网关契约](gateway-contract.md) 判断范围及副作用，再按 [运行时配置](runtime-configuration.md) 选择环境。

源码行号为快照定位，可能随源文件变更移动；调用链仅列出 Controller 中可识别的直接 Service/Mapper/Client 调用，未展开内部全部逻辑。
