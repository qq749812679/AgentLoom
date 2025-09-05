## 协议 / 安全 / 评测

### 协议设计
- 任务请求：`{goal, constraints, assets, preferences, context}`
- 工具调用：JSON Schema 限定，强校验与回放
- 事件与状态：`started/progress/done/error` + 指标
- 断点恢复：任务ID + 幂等 Replay（基于缓存与日志）

### 安全
- Prompt 侧：注入安全前缀/负面词、主题白/黑名单
- 输出侧：NSFW/仇恨检测、版权相似度（图像指纹/音频指纹）
- 资产侧：来源/授权元数据、风格冲突提醒

### 评测
- 合成：CLIPScore、Aesthetic Score、Music tagging
- 人评：成对比较与偏好学习，RRHF/Direct Preference
- 线上：质量监控、灰度发布、回滚策略


