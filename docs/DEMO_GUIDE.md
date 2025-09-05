# Demo 指南

## Web UI（Streamlit）

1. 安装依赖
   - Windows: `powershell -ExecutionPolicy Bypass -File setup.ps1`
   - macOS/Linux: `bash setup.sh`
2. 启动应用
   - `streamlit run app.py`
3. 打开浏览器访问 `http://localhost:8501`
4. 推荐体验路径
   - 文本 → 图像 → 音乐 → 灯光 → 视频
   - 试用场景："Create a cozy Christmas scene"

## CLI Demo（脚本）

1. 进入虚拟环境后执行：
   - `python scripts/demo_generator.py --prompt "sunset city" --length 12`
2. 产物位置：`multiscen/outputs`
3. 可选：启用 Mock API (`docker-compose up -d mock-api`) 来获得本地模型回路

## 远程部署（可选）

- Docker Compose: `docker-compose up -d`
- 前端开发：`cd frontend && npm install && npm start`

## 常见问题

- 端口冲突：修改 `.env` 中端口或关闭占用进程
- 缺少 ffmpeg：安装系统依赖后重试视频生成 