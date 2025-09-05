# 🚀 Quick Start Guide

Get up and running with the Multi-Modal AI Orchestrator in under 5 minutes!

## 📋 Prerequisites

- **Python 3.9+** ([Download here](https://python.org))
- **Git** ([Download here](https://git-scm.com))
- **FFmpeg** (optional, for video features)

## ⚡ One-Command Setup

```bash
# Clone and setup everything automatically
git clone https://github.com/yourusername/multi-modal-ai-orchestrator.git
cd multi-modal-ai-orchestrator
./setup.sh
```

The setup script will:
- ✅ Check Python version
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Create necessary directories
- ✅ Setup configuration files

## 🐳 Docker Setup (Alternative)

Prefer containers? Use Docker:

```bash
# Pull and run with docker-compose
docker-compose up -d

# Access at http://localhost:8501
```

## 🎯 First Run

1. **Start the application:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser to:** `http://localhost:8501`

3. **Follow the onboarding guide** - it'll walk you through:
   - Understanding the features
   - Setting your preferences  
   - Creating your first AI content
   - Optional device setup

## 🎨 Your First Creation

Let's create a complete audio-visual experience:

### 1. Text-to-Everything
1. Go to the **"🎨 智能创作"** tab
2. Enter a theme like "cozy winter evening"
3. Click **"🚀 开始创作"**
4. Watch as AI generates:
   - 🖼️ A beautiful scene image
   - 🎵 Matching background music  
   - 💡 Synchronized lighting program
   - 🎬 Combined video (optional)

### 2. Image-to-Music
1. Switch to **"🖼️ 图片驱动"** tab
2. Upload any photo
3. AI analyzes colors and mood
4. Generates matching soundtrack
5. Creates lighting that matches both

### 3. Music-to-Lights
1. Go to **"🎵 音乐驱动"** tab
2. Upload an audio file (.wav, .mp3)
3. AI analyzes the music
4. Creates dynamic lighting choreography
5. Export as WLED preset for real devices

## 🔧 Configuration (Optional)

Edit the `.env` file to enable advanced features:

```bash
# OpenAI for LLM features (recommended)
OPENAI_API_KEY=your_key_here

# Smart device integration
HUE_BRIDGE_IP=192.168.1.100
HUE_USERNAME=your_hue_username
WLED_IP=192.168.1.101

# Remote AI models (optional)
IMAGE_GENERATION_URL=http://your-server/txt2img
MUSIC_GENERATION_URL=http://your-server/musicgen
```

## 🤖 Advanced Features

### AI Agent Orchestration
- **"🤖 AI编排"** - Basic multi-agent workflows
- **"🧠 LangGraph"** - LLM-powered intelligent planning

### Multi-Room Control
- **"🏠 多房间"** - Design lighting for entire home
- Define rooms, themes, and synchronized programs

### Collaboration
- **"🤝 分享协作"** - Real-time team editing
- Share projects, collaborate live, browse community creations

## 📱 Smart Device Setup

### Philips Hue
1. Find your bridge IP: Use Hue app or router admin
2. Create username: Follow [Philips guide](https://developers.meethue.com/develop/get-started-2/)
3. Add to `.env` file
4. Test in **"⚡ 设备控制"** tab

### WLED
1. Flash WLED to ESP32/ESP8266
2. Configure WiFi and note IP address
3. Add IP to `.env` file
4. Test connection in device control tab

## 🎓 Learning Path

### Beginner (Week 1)
- [x] Complete onboarding
- [x] Create first text-to-everything project
- [x] Try image and music uploads
- [x] Explore different themes and styles

### Intermediate (Week 2)
- [ ] Connect smart devices
- [ ] Try multi-room projects
- [ ] Use advanced parameters
- [ ] Share your first creation

### Advanced (Week 3+)
- [ ] Create custom plugins
- [ ] Use LangGraph orchestration
- [ ] Set up collaboration workspace
- [ ] Contribute to the project

## 🆘 Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Slow generation speeds:**
- Enable caching in settings
- Use lower quality settings for testing
- Check internet connection for remote models

**Device connection fails:**
- Verify IP addresses are correct
- Check firewall settings
- Ensure devices are on same network

**UI not loading:**
- Clear browser cache
- Try incognito/private mode
- Check console for JavaScript errors

### Getting Help

- 📖 **Documentation**: Browse the `/docs` folder
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/multi-modal-ai-orchestrator/issues)
- 💬 **Discord**: Join our community chat
- 📧 **Email**: contact@your-project.com

## 🎉 What's Next?

Now that you're set up:

1. **Explore**: Try all the different generation modes
2. **Customize**: Adjust parameters to match your style
3. **Connect**: Link your smart home devices
4. **Share**: Join the community and share your creations
5. **Contribute**: Help make the project even better!

## 📚 Additional Resources

- [📖 Full Documentation](./README.md)
- [🏗️ Architecture Guide](./ARCHITECTURE.md)
- [🤖 Agent System](./AGENTS.md)
- [🔌 Plugin Development](./PLUGINS.md)
- [🤝 Contributing Guide](../CONTRIBUTING.md)

---

**Welcome to the future of AI-powered creativity! 🚀**

Questions? Ideas? We'd love to hear from you in our community channels!
