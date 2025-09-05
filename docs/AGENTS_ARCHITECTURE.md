## 多模态多 Agent 架构

### 目标
将语音-文字-图片-视频-音乐-灯光统一到一套可编排的多 Agent 系统，支持自治规划、工具调用、跨模态对齐、用户偏好学习与安全合规。

### 角色（可扩展）
- Orchestrator（编排/路由）：解析用户意图，分配子任务，融合结果
- Preference Agent（偏好学习）：建模用户品味，生成个性化约束与模板
- Vision Agent（图像）：文生图、图生图、检索、关键物体/风格识别
- Audio Agent（音乐/声音）：文生乐、图生乐、乐理分析、响度对齐
- Speech Agent（语音）：STT/TTS、说话人识别、情绪检测
- Video Agent（视频）：文生视频、图/音驱动视频、镜头规划与剪辑
- Lighting Agent（灯光）：场景/音乐驱动灯光生成，设备控制策略
- Safety Agent（安全/合规）：审查输出、过滤敏感内容、版权检测
- Memory Agent（短中长期记忆）：对话和历史项目上下文的结构化与检索
- Tools Agent（工具集合）：检索、翻译、OCR、MIDI/DMX 工具，文件读写

### 数据与记忆
- 短期会话记忆：当前会话目标、约束、已生成资产路径
- 中期项目记忆：项目级偏好、主题集、成功作品特征
- 长期用户画像：跨项目统计、偏好演化曲线、AB 测试结果
- 技术实现：矢量库（qdrant/pgvector），元数据存储（sqlite/postgres），RAG 检索

### 编排与协议
- 规划：CoT/ToT/GoT + 任务图（DAG），关键节点设置质量门控
- 通信：JSON RPC/消息总线（Redis/Kafka）+ 事件（started/progress/done/fail）
- 工具化：OpenAI function schema / JSON 模式约束，强约束解析
- 反馈：自评+互评+人类反馈（RRHF/Direct Preference），自动重试与候选集投票

### 评测与监控
- 质量：图像（CLIPScore/BLIP2 评审）、音乐（节拍一致性/主观评分）、视频（镜头连贯性）
- 可靠性：成功率/重试率/时延分布/超时率
- 安全：敏感命中率、误杀率、版权冲突率
- 业务：留存/转化/创作时长/复用率


