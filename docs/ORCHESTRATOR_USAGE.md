## Orchestrator 使用说明（MVP）

入口：UI 第四个 Tab “多Agent编排”。

工作流：
- 文本→图片/音乐/灯光：安全检查→图片合成→音乐合成→灯光生成→落盘
- 图片→音乐/灯光：音乐合成（图像特征）→灯光生成→落盘

实现：`mscen/agents/orchestrator.py`
- SafetyAgent：简单关键字过滤（可替换为更强模型）
- MemoryAgent：会话级键值存储（可替换为向量记忆/RAG）
- Orchestrator：编排各模块，统一输出路径

后续：
- 引入真实后端（SDXL/MusicGen/Whisper/TTS/Video）与质量门控
- 引入 DAG/队列与事件回调，实现长任务与断点恢复


