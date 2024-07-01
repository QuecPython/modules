# 独立功能模块

中文 | [English](./readme.md)

## 概述

- 该项目将不同的功能进行了独立的封装，每个文件都是一个单独的模块，可以进行独立使用。
- 所有模块都采用了观察者模式的设计方式。
- 模块之间的组合使用可使用注册观察者和被观察者的方式进行组合使用（使用回调的方式进行信息的通知），将模块之间的耦合性降到最低。

**模块列表：**

|模块|简介|说明|
|:---|---|---|
|aliIot.py|阿里物联网模块|该模块用于提供阿里云物联网模块相关功能，MQTT 协议的消息发布与订阅，OTA 升级。|
|battery.py|电池管理模块|该模块用于查询当前设备的电池电量与电压，设备的充电状态。|
|buzzer.py|蜂鸣器管理模块|该模块功能用于控制模块蜂鸣器的开关与周期性开关。|
|common.py|公告方法模块|该模块封装了一些公用组件与基类，方便其他模块使用。|
|history.py|历史文件模块|该模块主要用于读取记录与清理历史数据文件。|
|led.py|LED管理模块|该模块功能用于控制模块 LED 灯的开关与周期性闪烁。|
|location.py|定位管理模块|本模块提供了 GNSS 定位，基站定位，Wifi 定位三种定位模式的功能封装，提供了 WGS-84 转 GCJ-02 坐标系的转换方法。|
|logging.py|日志模块|该模块用于代码日志打印。|
|net_manage.py|网络管理模块|该模块用于管理设备网络相关功能，如：驻网，拨号，网络状态查询等。|
|player.py|音频播放|支持歌单循环播放、停止，支持单播放。|
|power_manage.py|低功耗管理|提供定时低功耗唤醒功能，当设备不进行业务处理时，可将设备调整为低功耗模式，当设备唤醒时，可通知用户进行业务处理。|
|serial.py|串口通信模块|实现阻塞读。|
|temp_humidity_sensor.py|温湿度传感器模块|该模块用于读取温湿度传感器数据。|
|thingsboard.py|ThingsBoard 平台|该模块用于提供物联网模块相关功能，MQTT 协议的消息发布与订阅。|

## 用法

- [aliIot API参考手册](./docs/zh/aliIot_API参考手册.md)
- [battery API参考手册](./docs/zh/battery_API参考手册.md)
- [buzzer API参考手册](./docs/zh/led&buzzer_API参考手册.md)
- [common API参考手册](./docs/zh/common_API参考手册.md)
- [history API参考手册](./docs/zh/history_API参考手册.md)
- [led API参考手册](./docs/zh/led&buzzer_API参考手册.md)
- [location API参考手册](./docs/zh/location_API参考手册.md)
- [logging API参考手册](./docs/zh/logging_API参考手册.md)
- [net_manage API参考手册](./docs/zh/net_manage_API参考手册.md)
- [player API参考手册](./docs/zh/player_API参考手册.md)
- [power_manage API参考手册](./docs/zh/power_manage_API参考手册.md)
- [serial API参考手册](./docs/zh/serial_API参考手册.md)
- [temp_humidity_sensor API参考手册](./docs/zh/temp_humidity_sensor_API参考手册.md)
- [thingsboard API参考手册](./docs/zh/thingsboard_API参考手册.md)

## 贡献

我们欢迎对本项目的改进做出贡献！请按照以下步骤进行贡献：

1. Fork 此仓库。
2. 创建一个新分支（`git checkout -b feature/your-feature`）。
3. 提交您的更改（`git commit -m 'Add your feature'`）。
4. 推送到分支（`git push origin feature/your-feature`）。
5. 打开一个 Pull Request。

## 许可证

本项目使用 Apache 许可证。详细信息请参阅 [LICENSE](./LICENSE) 文件。

## 支持

如果您有任何问题或需要支持，请参阅 [QuecPython 文档](https://python.quectel.com/doc) 或在本仓库中打开一个 issue。
