#!/bin/bash

# 🚀 Multi-Modal AI Orchestrator Setup Script
# This script sets up everything you need to run the project

set -e  # Exit on any error

echo "🌟 Welcome to Multi-Modal AI Orchestrator Setup!"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.9+ is installed
check_python() {
    print_status "Checking Python version..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if python3 -c 'import sys; exit(sys.version_info < (3, 9))'; then
            print_success "Python $PYTHON_VERSION found"
            PYTHON_CMD="python3"
        else
            print_error "Python 3.9+ required, found $PYTHON_VERSION"
            exit 1
        fi
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        if python -c 'import sys; exit(sys.version_info < (3, 9))'; then
            print_success "Python $PYTHON_VERSION found"
            PYTHON_CMD="python"
        else
            print_error "Python 3.9+ required, found $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python not found. Please install Python 3.9+"
        exit 1
    fi
}

# Create virtual environment
setup_venv() {
    print_status "Setting up virtual environment..."
    if [ ! -d ".venv" ]; then
        $PYTHON_CMD -m venv .venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source .venv/Scripts/activate
    else
        source .venv/bin/activate
    fi
    print_success "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    print_success "Dependencies installed"
}

# Create necessary directories
create_directories() {
    print_status "Creating project directories..."
    mkdir -p outputs logs user_profiles shared feedback memory plugins
    print_success "Directories created"
}

# Setup environment file
setup_env() {
    print_status "Setting up environment configuration..."
    if [ ! -f ".env" ]; then
        cat > .env << EOL
# Multi-Modal AI Orchestrator Configuration

# OpenAI Configuration (Optional - for LLM features)
OPENAI_API_KEY=your_openai_api_key_here

# Model Endpoints (Optional - for remote AI models)
IMAGE_GENERATION_URL=http://localhost:8000/txt2img
MUSIC_GENERATION_URL=http://localhost:8000/musicgen
STT_URL=http://localhost:8000/stt
TTS_URL=http://localhost:8000/tts

# Device Configuration (Optional - for smart lights)
HUE_BRIDGE_IP=192.168.1.100
HUE_USERNAME=your_hue_username
WLED_IP=192.168.1.101

# Development Settings
DEBUG=true
LOG_LEVEL=INFO
CACHE_ENABLED=true
EOL
        print_success "Environment file created (.env)"
        print_warning "Please edit .env file with your API keys and device settings"
    else
        print_warning "Environment file already exists"
    fi
}

# Check for optional dependencies
check_optional_deps() {
    print_status "Checking optional dependencies..."
    
    # Check for ffmpeg
    if command -v ffmpeg &> /dev/null; then
        print_success "FFmpeg found - video generation enabled"
    else
        print_warning "FFmpeg not found - video generation will be limited"
        print_status "Install with: brew install ffmpeg (macOS) or apt install ffmpeg (Ubuntu)"
    fi
    
    # Check for Docker
    if command -v docker &> /dev/null; then
        print_success "Docker found - containerized deployment available"
    else
        print_warning "Docker not found - install for easier deployment"
    fi
}

# Run initial tests
run_tests() {
    print_status "Running basic health checks..."
    
    # Test Python imports
    $PYTHON_CMD -c "
import streamlit
import PIL
import numpy
import scipy
print('✅ Core dependencies working')
"
    
    print_success "Health checks passed"
}

# Display setup completion
show_completion() {
    echo ""
    echo "🎉 Setup Complete!"
    echo "=================="
    echo ""
    echo "Next steps:"
    echo "1. Edit .env file with your API keys (optional)"
    echo "2. Run the application:"
    echo "   streamlit run app.py"
    echo ""
    echo "3. Open your browser to: http://localhost:8501"
    echo ""
    echo "📖 Documentation: ./docs/"
    echo "🐛 Issues: https://github.com/yourusername/multi-modal-ai-orchestrator/issues"
    echo "💬 Discord: https://discord.gg/your-discord"
    echo ""
    echo "Happy creating! 🚀"
}

# Main setup function
main() {
    echo "Starting setup process..."
    echo ""
    
    check_python
    setup_venv
    activate_venv
    install_dependencies
    create_directories
    setup_env
    check_optional_deps
    run_tests
    show_completion
}

# Run setup
main
