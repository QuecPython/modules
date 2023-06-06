# 串口通信模块 用户指导手册

## 简介

> 基于`audio`模块的简略封装。支持歌单播放、停止，单曲播放。

## 使用说明

1、初始化

```python
from player import Player
```

2、歌单无限循环播放

```python
# 列表歌单为文件路径，该列表会被无限循环迭代播放。
player.loop_play(['music1.mp3', 'music2.mp3'])
```

3、单曲播放

```python
player.play('music3.mp4')
```

> 注意：play和loop_play方法调用播放音频前，都会先停止正在播放的音频。

