# 音频播放模块 API 参考手册

中文 | [English](../en/player_API_Reference.md)

## 简介

> 基于 `audio` 模块的简略封装。支持歌单播放、停止，单曲播放。

## API 说明

### Player

> 功能模块初始化。

**注意：**

`play` 和 `loop_play` 方法调用播放音频前，都会先停止正在播放的音频。

**示例：**

```python
from player import Player
player = Player(device=0, pa_gpio=2)
```

**参数：**

| 参数    | 类型 | 说明                 |
| ------- | ---- | -------------------- |
| device  | int  | Audio通道号，默认为0 |
| pa_gpio | int  | 音量控制GPIO号       |

### Player.audio_cb

> 音频播放回调

**示例：**

```python
def audio_cb(self, event):
    if event == 0:
        logger.info('audio play start.')
    elif event == 7:
        logger.info('audio play finish.')
```

**参数：**

| 参数  | 类型 | 说明                                 |
| ----- | ---- | ------------------------------------ |
| event | int  | 事件类型（0：开始播放；1：结束播放） |

### Player.loop_play_executor

> 执行播放

**示例：**

```python
# 播放单首
player.loop_play('music1.mp3')
```

**参数：**

| 参数 | 类型 | 说明         |
| ---- | ---- | ------------ |
| song | str  | 音频文件路径 |

### Player.loop_play

> 歌单无限循环播放。

**示例：**

```python
# 列表歌单为文件路径，该列表会被无限循环迭代播放。
player.loop_play(['music1.mp3', 'music2.mp3'])
```

**参数：**

| 参数       | 类型 | 说明             |
| ---------- | ---- | ---------------- |
| song_sheet | list | 音频播放文件列表 |

### Player.play

> 单曲播放。

**示例：**

```python
player.play('music3.mp4')
```

**参数：**

| 参数 | 类型 | 说明         |
| ---- | ---- | ------------ |
| song | str  | 音频文件路径 |

### Player.stop

> 停止播放

### Player.setVolume

> 设置音量

**示例：**

```python
# 设置音量级别为11
player.setVolume(11)
```

**参数：**

| 参数  | 类型 | 说明                           |
| ----- | ---- | ------------------------------ |
| level | int  | level: 0~11音量大小，0表示静音 |

