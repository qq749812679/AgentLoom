# 🌟 Multi‑Modal AI Orchestrator

[简体中文](README.zh-CN.md) | English

<div align="center">

![Banner](https://img.shields.io/badge/Multi--Modal-AI%20Orchestrator-blue?style=for-the-badge&logo=robot&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-18.2+-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![LangGraph](https://img.shields.io/badge/LangGraph-🦜-green?style=for-the-badge)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)

**The Agentic OS for synchronized TEXT 。Image · Music · Lights · Video**

From one prompt to an immersive, production‑ready experience — with real devices.


<a href="https://qq749812679.github.io/Multi-Modal-AI-Orchestrator" target="_blank"><img src="https://img.shields.io/badge/Docs-Read%20the%20Docs-blue?style=for-the-badge" /></a>
<a href="#" target="_blank"><img src="https://img.shields.io/badge/Demo-Open%20Live%20Demo-orange?style=for-the-badge" /></a>

</div>

---

## 🚀 Why this project stands out

- 🧠 **Agentic orchestration, not scripts**: LangGraph‑based multi‑agent planning with memory, feedback, safety and collaboration.
- 🎛️ **Text‑to‑Everything pipeline**: One workflow to generate image, compose music, choreograph lights, and render video.
- 💡 **Device‑native**: First‑class Philips Hue / WLED control. Not just a demo — it runs your room.
- 🔌 **Pluggable backends**: SD WebUI / HTTP models hot‑swappable with latency/cost profiling and health probing.
- 🧪 **Feedback → Auto‑tuning**: Collect ratings, learn patterns, and surface optimization suggestions automatically.
- 📦 **Task queue UX**: Pause / resume / retry with persistent progress cards.
- 🧭 **First‑run wizard**: Writes .env + device params in minutes.
- 🏢 **Enterprise‑ready knobs**: License gating, audit logs, role‑based hooks.

## ✨ What you can build in 60 seconds

- “Cozy jazz bar” → cinematic image + mellow soundtrack + warm lighting show + MP4
- Upload a photo → matching soundtrack + mood‑aligned lighting
- Drop a song → beat‑synced lighting with presets for Hue/WLED

## ⚡ Quick start

### Windows (PowerShell)
1. `cd multiscen`
2. `powershell -ExecutionPolicy Bypass -File setup.ps1`
3. `streamlit run app.py`

### macOS/Linux
1. `cd multiscen && bash setup.sh`
2. `streamlit run app.py`

### Optional frontend (React)
- `cd multiscen/frontend && npm install && npm start`

### CLI
- `mscen gen "sunset jazz bar" --video`
- `mscen list`

## 🥊 How it beats typical alternatives

- **Unified multi‑modal pipeline** vs single‑modality generators (image‑only or music‑only)
- **Device‑native control** vs pure screen previews
- **Agentic planning + feedback learning** vs manual trial‑and‑error
- **Latency/cost profiling + task queue** vs blind requests with no operational UX
- **Onboarding wizard** vs hand‑editing envs and YAMLs

## 🧩 Architecture at a glance

- Backend: Streamlit + FastAPI + LangGraph, feedback learner, model optimizer
- Frontend: React + TypeScript + Tailwind, real‑time agent/queue views
- Connectors: SD WebUI, HTTP image/music/STT/TTS, Hue/WLED devices
- Enterprise: License server, audit logger, security hooks

## 🧪 Live demos

- Web UI: Text‑to‑Everything studio, real‑time device control
- Mock API: `docker-compose up -d mock-api`
- Short video/GIFs: coming soon (PRs welcome!)

## 🛣️ Roadmap highlights

- Strategy‑based routing (lowest latency / lowest cost / balanced)
- Auto‑tuned parameter replay ("apply suggestions" one‑click)
- Multi‑user spaces and approval workflows

## 🤝 Contribute & grow with us

- Star ⭐ if this saves your time, PRs welcome!
- Use Issues for bugs/ideas, Discussions for design talks
- Sponsors/Backers: see `.github/FUNDING.yml`

## 📄 License

MIT — build amazing things.
