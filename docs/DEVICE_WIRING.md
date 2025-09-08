# Wiring & Safety (GPIO/USB, Raspberry Pi & Arduino)

> Disclaimer: Always follow electrical safety. For mains voltage, use certified power supplies and isolation.

## GPIO (Raspberry Pi)
- Use 3.3V logic; add MOSFET driver for LED strips or relay modules
- Example mapping:
  - GPIO18 (PWM) → LED strip (via MOSFET)
  - GPIO17 → Relay IN1 (5V relay board with transistor)
- Power: Prefer external 5V/12V PSU for LED strips; common ground with Pi

## USB (Arduino/USB-DMX)
- Arduino over USB serial for motor/relay/analog sensors
- USB-DMX interface to stage lights (512 channels)
- Protocol: simple JSON lines `{ "channel": 1, "value": 128 }`

## Hue/WLED
- Hue: Bridge IP + Username, scenes via API
- WLED: HTTP JSON API; segment and effect presets

## Safety limits
- Max brightness/night mode; thermal throttling; watchdog to turn lights off on error

## Example .env
```
HUE_BRIDGE_IP=192.168.1.100
HUE_USERNAME=your_hue_username
WLED_IP=192.168.1.101
GPIO_ENABLED=true
ARDUINO_SERIAL=COM3  # or /dev/ttyUSB0
``` 