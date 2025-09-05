## 多模态与 Agent 技术栈

### 模型层
- 文本/对话：GPT-4o/Claude/自部署 Llama/DeepSeek，函数调用与JSON约束
- 图像：SDXL/Flux/Stable Diffusion Turbo，ControlNet/LoRA
- 音乐/音频：MusicGen/AudioLDM/AudioCraft，RVC/So-VITS 变声
- 语音：WhisperX/NeMo/Edge STT；Edge TTS/ElevenLabs TTS
- 视频：Sora/Gen-3/Stable Video Diffusion；Pika/Runway 工具链

### 中间件
- 工作流：Temporal/Prefect/Airflow（任务编排与重试）
- 向量检索：Qdrant/Weaviate/PGVector
- 消息队列：Redis/Kafka；事件总线与流处理
- 存储：对象存储（S3/MinIO）、数据库（Postgres/SQLite）

### 工具与推理
- 图片工具：rembg、CLIP/BLIP2 评审、超分/去噪
- 音乐工具：MIDI 解析/量化、节拍/Key 检测、响度标准化（EBU R128）
- 视频工具：镜头切分、字幕/OCR、节奏对齐编辑
- 灯光工具：WLED/Hue/Yeelight/DMX/sACN 控制库

### 代理能力
- 计划/反思：CoT/ToT/GoT、自监督反思（Reflexion）
- 记忆：短中长期记忆层；RAG + 结构化索引
- 角色化：系统与工具提示工程、风格模板、约束规则
- 安全：多级过滤（Prompt/Output/Asset）、版权检测/指纹对比


