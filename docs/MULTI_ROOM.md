## 多房间项目（v3）

- Schema：`Project{name, theme, rooms[]}`；`Room{name, brightness, delay_ms}`
- 编译：基于主题生成基线节目，按房间亮度缩放与延时合成
- 导出：每房间一份 JSON；可扩展导出 WLED/Hue/DMX 等协议

使用：UI 第五个 Tab，设置项目、房间数量与参数，点击编译导出。
