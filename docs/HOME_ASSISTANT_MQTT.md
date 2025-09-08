# Home Assistant & MQTT Integration

## Home Assistant
- Expose scenes and recipes as Home Assistant scripts
- Use REST or MQTT discovery to register entities
- Example REST call to trigger a recipe:
```
POST http://localhost:8000/api/recipe/apply
Body: { "name": "rainy_reading_room" }
```

## MQTT
- Topics:
  - `agentloom/command` → input commands `{ type, payload }`
  - `agentloom/status` → job/agent/device updates
- Example publish (lights):
```
{ "type": "lights.scene", "payload": { "scene": "warm_breathe", "brightness": 60 } }
```

## Security
- Use username/password or TLS
- Rate limit and schema-validate inbound messages 