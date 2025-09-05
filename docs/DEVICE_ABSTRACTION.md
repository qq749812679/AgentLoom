## 设备抽象（适配层）

接口目标：统一将灯光节目帧序列输出到不同设备/协议。

抽象：
```python
class LightDevice:
    def connect(self): ...
    def send_frame(self, r:int, g:int, b:int, ms:int): ...
    def close(self): ...
```

实现（示例）：
- `HueDevice`：Bridge IP、用户名；循环推送颜色与过渡
- `YeelightDevice`：LAN 协议，`set_rgb`+过渡
- `WLEDDevice`：HTTP JSON（/json/state），或 UDP 实时
- `DMXDevice`：sACN/ArtNet/USB-DMX，通道映射（R/G/B）

后续可在 `mscen/devices/` 增加具体实现与配置机制。



