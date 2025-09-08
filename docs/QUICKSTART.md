# Quick Start

This guide helps you run the system and try the new multi-modal, synchronized features.

## Run the app

### Windows (PowerShell)
1. `cd multiscen`
2. `powershell -ExecutionPolicy Bypass -File setup.ps1`
3. `streamlit run app.py`

### macOS/Linux
1. `cd multiscen && bash setup.sh`
2. `streamlit run app.py`

### Optional frontend (React)
- `cd multiscen/frontend && npm install && npm start`

## CLI examples
- `mscen gen "rainy reading room" --video`
- `mscen list`

## What’s next
- See Wiring & Safety for GPIO/USB setup
- See Home Assistant / MQTT integration
- Try Quick Demos to validate sync across Image/Music/Lights/Video
