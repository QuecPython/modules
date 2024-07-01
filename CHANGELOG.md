# ChangeLog

[中文](./CHANGELOG_ZH.md) | English

All notable changes to this project will be documented in this file.

## [v.1.2.2] - 2023-06-06

### Added

- **player.py Player (based on audio implementation)**

### Changed

- **serial.py Module** General condition variable definitions moved to the common.py module

## [v.1.2.1] - 2023-05-26

### Added

- **serial.py** Serial communication module

## [v.1.2.0] - 2023-04-14

### Added

- **buzzer.py** Buzzer module
- **net_manage.py** Network management module
- **power_manage.py** Low power management module
- **thingsboard.py** ThingsBoard client module
- **temp_humidity_sensor.py** Temperature and humidity sensor module

### Changed

- **aliyunIot.py** Aliyun module, adjusted functionality architecture and interface
- **battery.py** Battery module, adjusted functionality architecture and interface
- **common.py** Common functionality module, adjusted common module
- **led.py** LED module, adjusted functionality architecture
- **location.py** Location module, adjusted functionality architecture
- **logging.py** Logging module, adjusted functionality architecture

### Deleted

- **mpower.py** Old low power management module
- **quecthing.py** Quecthing module

## [v1.1.0] - 2022-12-21

### Changed

- Function optimization and architecture adjustment

## [v1.0.0] - 2022-05-09

### Added

- Added Aliyun module, battery module, historical file module, LED module, location module, logging module, low power sleep module, cloud interaction middleware module