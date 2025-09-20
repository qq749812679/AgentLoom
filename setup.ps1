Param()

$ErrorActionPreference = "Stop"

function Write-Info($msg) { Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Ok($msg)   { Write-Host "[OK]   $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "[ERR]  $msg" -ForegroundColor Red }

Write-Host "🌟 AgentLoom｜灵构织机 Setup (Windows)" -ForegroundColor Magenta

# 1) Check Python >= 3.9
Write-Info "Checking Python version..."
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { Write-Err "未检测到 Python，请安装 Python 3.9+"; exit 1 }
$ver = (& python -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
if (-not $ver) { Write-Err "无法获取 Python 版本"; exit 1 }
$major,$minor = $ver.Split('.')
if ([int]$major -lt 3 -or ([int]$major -eq 3 -and [int]$minor -lt 9)) {
  Write-Err "需要 Python 3.9+，当前为 $ver"; exit 1
}
Write-Ok "Python $ver"

# 2) Create venv
Write-Info "Creating virtual environment (.venv)..."
if (-not (Test-Path .venv)) {
  python -m venv .venv
  Write-Ok "venv created"
} else {
  Write-Warn ".venv 已存在"
}

# 3) Activate venv
Write-Info "Activating venv..."
$activate = Join-Path .venv "Scripts/Activate.ps1"
if (-not (Test-Path $activate)) { Write-Err "未找到 Activate.ps1"; exit 1 }
. $activate
Write-Ok "venv activated"

# 4) Install deps
Write-Info "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
Write-Ok "Dependencies installed"

# 5) Create directories
Write-Info "Creating directories..."
$dirs = @("outputs","logs","user_profiles","shared","feedback","memory","plugins")
foreach ($d in $dirs) { if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d | Out-Null } }
Write-Ok "Directories ready"

# 6) .env template
Write-Info "Preparing .env..."
if (-not (Test-Path ".env")) {
  @"
# AgentLoom｜灵构织机 Configuration
OPENAI_API_KEY=your_openai_api_key_here
IMAGE_GENERATION_URL=http://localhost:8000/txt2img
MUSIC_GENERATION_URL=http://localhost:8000/musicgen
STT_URL=http://localhost:8000/stt
TTS_URL=http://localhost:8000/tts
HUE_BRIDGE_IP=192.168.1.100
HUE_USERNAME=your_hue_username
WLED_IP=192.168.1.101
DEBUG=true
LOG_LEVEL=INFO
CACHE_ENABLED=true
"@ | Out-File -Encoding UTF8 .env
  Write-Ok ".env created (请按需修改)"
} else {
  Write-Warn ".env 已存在"
}

# 7) Health check
Write-Info "Running health check..."
python -c "
import streamlit, PIL, numpy, scipy
print('✅ Core dependencies working')
"
Write-Ok "Setup complete"

Write-Host "下一步：`n1) 修改 .env 填写你的 Key (可选)`n2) 启动后端： streamlit run app.py`n3) 访问 http://localhost:8501" -ForegroundColor Cyan 