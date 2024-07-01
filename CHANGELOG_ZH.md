# ChangeLog

中文 | [English](./CHANGELOG.md)

此项目的所有显着更改都将记录在此文件中。

## [v.1.2.2] - 2023-06-06

### Added

- **player.py 播放器（基于audio实现）**

### Changed

- **serial.py 模块通用条件变量定义移至common.py模块中**

## [v.1.2.1] - 2023-05-26

### Added

- **serial.py** 串口通信模块

## [v.1.2.0] - 2023-04-14

### Added

- **buzzer.py** 蜂鸣器模块
- **net_manage.py** 网络管理模块
- **power_manage.py** 低功耗管理模块
- **thingsboard.py** ThingsBoard客户端模块
- **temp_humidity_sensor.py** 温湿度传感器模块

### Changed

- **aliyunIot.py** 阿里云模块, 调整了功能架构与接口
- **battery.py** 电池模块, 调整功能架构与接口
- **common.py** 通用功能模块, 调整通用模块
- **led.py** LED模块, 调整功能架构
- **location.py** 定位模块, 调整功能架构
- **logging.py** 日志模块, 调整功能架构

### Deleted

- **mpower.py** 老低功耗管理模块
- **quecthing.py*** 移远云模块

## [v1.1.0] - 2022-12-21

### Changed

- 功能优化与架构调整

## [v1.0.0] - 2022-05-09

### Added

- 添加了阿里云模块，电池模块，历史文件模块，LED模块，定位模块，日志模块，低功耗休眠模块，云端交互中间层模块
