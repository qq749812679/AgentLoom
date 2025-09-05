## LangGraph + MCP 集成说明（MVP）

### LangGraph
- 入口：UI 第七个 Tab“LangGraph编排”
- 当前实现：无LLM的简化 Planner（可替换为 OpenAI 规划）
- 扩展：在 plan_node 中调用 OpenAI，将 `{goal, context}` 转为任务列表

### MCP Tools Server
- 位置：`server/mcp_server.py`，FastAPI 暴露 `/tools/*`
- 工具：`txt2img`、`music`、`lighting`
- 启动：`uvicorn server.mcp_server:app --reload --port 8002`

### 环境变量
```
OPENAI_API_KEY=sk-...
SDWEBUI_URL=http://localhost:7860
IMAGE_TXT2IMG_URL=http://localhost:8001
MUSIC_GEN_URL=http://localhost:8001
STT_URL=http://localhost:8001
TTS_URL=http://localhost:8001
```

### 后续
- 将 LangGraph 的 plan 节点升级为 LLM 规划 + 反思；错误时降级到启发式
- 将 MCP 工具接入真实后端与鉴权；丰富工具：视频、WLED/Hue 等


