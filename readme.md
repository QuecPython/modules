# Independent Function Module

[中文](./README_ZH.md) | English

## Introduction

- This project encapsulates different functions independently. Each file is a separate module and can be used independently.
- All modules are designed using the observer pattern.
- Modules can be used in combination by registering observers and observed objects (using callbacks to notify information) to minimize the coupling between modules.

## Modules

|Module|Introduction|Description|
|:---|---|---|
|aliIot.py|Alibaba Internet of Things module|This module is used to provide functions related to the Alibaba Cloud IoT module, message publishing and subscription of the MQTT protocol, and OTA upgrades. |
|battery.py|Battery management module|This module is used to query the battery power and voltage of the current device, and the charging status of the device. |
|buzzer.py|Buzzer management module|This module function is used to control the switch and periodic switch of the module buzzer. |
|common.py|Announcement method module|This module encapsulates some public components and base classes to facilitate the use of other modules. |
|history.py|History file module|This module is mainly used to read records and clean historical data files. |
|led.py|LED management module|This module function is used to control the switching and periodic flashing of the module's LED lights. |
|location.py|Positioning management module|This module provides functional encapsulation of three positioning modes: GNSS positioning, base station positioning, and Wifi positioning, and provides a conversion method from WGS-84 to GCJ-02 coordinate system. |
|logging.py|Log module|This module is used for code log printing. |
|net_manage.py|Network management module|This module is used to manage device network-related functions, such as: network presence, dial-up, network status query, etc. |
|player.py|Audio playback|Supports song list loop playback, stop, and single playback. |
|power_manage.py|Low-power management|Provides scheduled low-power wake-up function. When the device is not performing business processing, the device can be adjusted to low-power mode. When the device wakes up, the user can be notified to perform business processing. |
|serial.py|Serial communication module|Realizes blocking reading. |
|temp_humidity_sensor.py|Temperature and humidity sensor module|This module is used to read temperature and humidity sensor data. |
|thingsboard.py|ThingsBoard Platform|This module is used to provide functions related to the Internet of Things module and message publishing and subscription of the MQTT protocol. |

## Usage

- [aliIot User Guide](./docs/en/aliIot_User_Guide.md)
- [battery User Guide](./docs/en/battery_User_Guide.md)
- [buzzer User Guide](./docs/en/buzzer_User_Guide.md)
- [common User Guide](./docs/en/common_User_Guide.md)
- [history User Guide](./docs/en/history_User_Guide.md)
- [led User Guide](./docs/en/led&buzzer_User_Guide.md)
- [location User Guide](./docs/en/location_User_Guide.md)
- [logging User Guide](./docs/en/logging_User_Guide.md)
- [net_manage User Guide](./docs/en/net_manage_User_Guide.md)
- [player User Guide](./docs/en/player_User_Guide.md)
- [power_manage User Guide](./docs/en/power_manage_User_Guide.md)
- [serial User Guide](./docs/en/serial_User_Guide.md)
- [temp_humidity_sensor User Guide](./docs/en/temp_humidity_sensor_User_Guide.md)
- [thingsboard User Guide](./docs/en/thingsboard_User_Guide.md)

## Contribution

We welcome contributions to improve this project! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

## License

This project is licensed under the Apache License. See the [LICENSE](./LICENSE) file for details.

## Support

If you have any questions or need support, please refer to the [QuecPython documentation](https://python.quectel.com/doc/en) or open an issue in this repository.
