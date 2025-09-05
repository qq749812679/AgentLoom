## 测试与验证

### 本地运行
1. `streamlit run app.py`
2. 选择预设主题生成，确认：
   - 图片可见、可下载
   - 音乐可播放、可下载
   - 灯光 JSON 可下载，预览条显示

### 单元测试建议（后续）
- `colors.palette_for_theme` 覆盖常见主题
- `music_gen._theme_to_scale`、节拍长度正确性
- `image_to_music._image_mood_params` 亮度对比度边界
- `lighting.generate_*` 帧数、字段校验

### 端到端测试建议
- 录制固定输入（prompt、图片）与固定随机种子
- 比较输出基本属性（尺寸、时长、帧数），而非逐样本比特相等


