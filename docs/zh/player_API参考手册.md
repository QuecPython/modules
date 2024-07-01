# 串口通信模块 API 参考手册

中文 | [English](../en/player_API_Reference.md)

## 简介

> 基于 `audio` 模块的简略封装。支持歌单播放、停止，单曲播放。

## API 说明

### Player

**注意：**

`play` 和 `loop_play` 方法调用播放音频前，都会先停止正在播放的音频。

> 功能模块初始化。

**示例：**

```python
from player import Player
player = Player()
```

### Player.loop_play

> 歌单无限循环播放。

**示例：**

```python
# 列表歌单为文件路径，该列表会被无限循环迭代播放。
player.loop_play(['music1.mp3', 'music2.mp3'])
```

### Player.play

> 单曲播放。

**示例：**

```python
player.play('music3.mp4')
```
