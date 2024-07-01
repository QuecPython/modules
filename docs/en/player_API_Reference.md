# Audio Playback Module API Reference Manual

[中文](../zh/player_API参考手册.md) | English

## Introduction

> A simplified encapsulation based on the `audio` module. Supports playlist playback, stopping, and single track playback.

## API Description

### Player

> Initialize the function module.

**Note:**

The `play` and `loop_play` methods will stop any currently playing audio before starting new playback.

**Example:**

```python
from player import Player
player = Player(device=0, pa_gpio=2)
```

**Parameters:**

| Parameter | Type | Description            |
| --------- | ---- | ---------------------- |
| device    | int  | Audio channel number, default is 0 |
| pa_gpio   | int  | Volume control GPIO number |

### Player.audio_cb

> Audio playback callback

**Example:**

```python
def audio_cb(self, event):
    if event == 0:
        logger.info('audio play start.')
    elif event == 7:
        logger.info('audio play finish.')
```

**Parameters:**

| Parameter | Type | Description                        |
| --------- | ---- | ---------------------------------- |
| event     | int  | Event type (0: start playback; 1: end playback) |

### Player.loop_play_executor

> Execute playback

**Example:**

```python
# Play a single track
player.loop_play('music1.mp3')
```

**Parameters:**

| Parameter | Type | Description       |
| --------- | ---- | ----------------- |
| song      | str  | Audio file path   |

### Player.loop_play

> Infinite loop playback of a playlist.

**Example:**

```python
# The playlist is a list of file paths, which will be played in an infinite loop.
player.loop_play(['music1.mp3', 'music2.mp3'])
```

**Parameters:**

| Parameter  | Type | Description           |
| ---------- | ---- | --------------------- |
| song_sheet | list | List of audio files   |

### Player.play

> Single track playback.

**Example:**

```python
player.play('music3.mp4')
```

**Parameters:**

| Parameter | Type | Description       |
| --------- | ---- | ----------------- |
| song      | str  | Audio file path   |

### Player.stop

> Stop playback

### Player.setVolume

> Set volume

**Example:**

```python
# Set volume level to 11
player.setVolume(11)
```

**Parameters:**

| Parameter | Type | Description                        |
| --------- | ---- | ---------------------------------- |
| level     | int  | Volume level: 0~11, where 0 means mute |