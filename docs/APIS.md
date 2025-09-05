## 模块接口（MVP）

### Image
`generate_scene_image(theme: str, size=(w,h)) -> PIL.Image`

### Music from Theme
`generate_music_from_theme(theme: str, duration_s: float, out_dir: Path) -> Path`

### Music from Image
`generate_music_from_image(img: PIL.Image, duration_s: float, out_dir: Path) -> Path`

### Lighting
`generate_lighting_from_theme(theme: str) -> List[Frame]`
`generate_lighting_from_image(img: PIL.Image) -> List[Frame]`
`save_lighting_program(frames, out_dir: Path) -> Path`

Frame 结构：`{"r":int, "g":int, "b":int, "ms":int}`


