# 🌟 多模态 AI 编排平台

[English README](README.md) | 简体中文

把“一个想法”变成“可看、可听、可控”的沉浸式体验：一条流水线完成 文字 + 图片 + 音乐 + 灯光 + 视频，并能直接操控 Hue/WLED 真设备。

---

## 为什么它与众不同

- 🧠 **Agent 智能编排**：基于 LangGraph 的多 Agent 规划，带记忆、反馈与安全约束。
- 🎛️ **文本到一切（Text‑to‑Everything）**：一次输入，产出图片、音乐、灯光、视频全链路结果。
- 💡 **真设备优先**：不仅是屏幕预览，直接接管 Philips Hue / WLED 房间灯光。
- 🔌 **后端可插拔**：SD WebUI / HTTP 模型随插随用，支持延迟/成本画像与健康探测。
- 🧪 **反馈→自动调参**：收集评分、学习偏好，自动给出优化建议与预计收益。
- 📦 **任务队列体验**：暂停/恢复/重试 + 持久进度卡片，真正可运营。
- 🧭 **首启向导**：一步写好 `.env` 与设备参数，新手 3 分钟起飞。
- 🏢 **企业能力**：License 开关、审计日志、权限钩子，易于内外网落地。

## 60 秒你能做什么

- “温暖爵士吧”→ 电影感图片 + 情绪契合音乐 + 暖色灯光编排 + MP4
- 上传一张图 → 生成匹配情绪的配乐 + 同步灯光
- 拖入一段歌 → 节拍对齐的灯光节目，导出 Hue/WLED 预设

## 快速开始

### Windows（PowerShell）
1. `cd multiscen`
2. `powershell -ExecutionPolicy Bypass -File setup.ps1`
3. `streamlit run app.py`

### macOS/Linux
1. `cd multiscen && bash setup.sh`
2. `streamlit run app.py`

### 可选前端（React）
- `cd multiscen/frontend && npm install && npm start`

### CLI
- `mscen gen "sunset jazz bar" --video`
- `mscen list`

## 它相对常见开源方案的优势

- **一体化多模态流水线**：不是“单模态拼拼凑凑”，而是端到端协同
- **设备原生**：直接驱动 Hue/WLED，体验落地到“房间里的光”
- **智能闭环**：Agent 规划 + 反馈学习 + 自动调参，减少反复试错
- **可运营的生产体验**：延迟/成本画像 + 任务队列 + 首启向导

## 架构速览

- 后端：Streamlit + FastAPI + LangGraph（反馈学习、模型优化）
- 前端：React + TypeScript + Tailwind（实时 Agent/队列可视化）
- 连接器：SD WebUI、HTTP 图像/音乐/STT/TTS、Hue/WLED 设备
- 企业：License Server、审计日志、Security Hooks

## Demo

- Web UI：文本→一切工作室、实时设备控制
- Mock API：`docker-compose up -d mock-api`
- 短视频/GIF：欢迎社区 PR 一起完善

## 路线图（节选）

- 策略路由：最低延迟/最低成本/平衡
- 一键“按建议重跑”（Auto‑Tune Replay）
- 团队空间与审批流

## 参与共建

- 如果它帮到你，请点个 ⭐ Star；欢迎提交 PR
- Bug/想法用 Issues，方案讨论走 Discussions
- 赞助/支持请见 `.github/FUNDING.yml`

## 保持领先

Star 本仓库以第一时间收到新版本与重要更新通知。

## 系统要求

- CPU ≥ 2 核
- 内存 ≥ 4 GiB
- Python ≥ 3.9（本地运行）
- Docker / Docker Compose（可选，容器化部署）

## Docker Compose 快速启动

在 `multiscen` 目录下：

```bash
cd multiscen
cp .env .env.backup  # 如无 .env，可先运行 setup.sh 自动生成
docker compose up -d
# 打开浏览器访问：http://localhost:8501
```

说明：Compose 将启动主应用（8501）、Redis（6379）与开发用 Mock API（8000）。如需生产入口，可启用 `nginx` profile 与证书目录。

## 社区与支持

- GitHub Issues：提交 Bug 与功能提案
- GitHub Discussions：分享使用案例与讨论方案
- 电子邮件：可在仓库简介中补充联系邮箱

## 安全问题

请勿在公开 Issue 披露安全漏洞。可参考仓库根目录 `SECURITY.md` 的上报方式。

## 许可证

MIT — 去创造更酷的多模态体验吧。 