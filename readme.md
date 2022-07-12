# 独立功能模块 API v2.1.0

## 简介

- 该项目将不同的功能进行了独立的封装，每个文件都是一个单独的模块，可以进行独立使用
- 所有模块都采用了观察者模式的设计方式
- 模块之间的组合使用可使用注册观察者和被观察者的方式进行组合使用，将模块之间的耦合性降到最低

## 模块列表

|模块|简介|说明|
|:---|---|---|
|aliyunIot|阿里云物联网模块|该模块用于提供阿里云物联网模块相关功能，MQTT协议的消息发布与订阅, OTA升级。|
|battery|设备电池模块|该模块用于查询当前设备的电池电量与电压，设备的充电状态。|
|common|公用模块|该模块封装了一些公用组件与基类，方便其他模块使用。|
|history|历史文件模块|该模块用于提供阿里云物联网模块相关功能，MQTT协议的消息发布与订阅该模块主要用于读取记录与清理历史数据文件，该模块设计成监听者模式，可以和`remote`模块结合使用，当`remote`发送消息失败时，将消息通知给`history`模块，存入历史文件中。|
|led|LED模块|该模块功能用于控制模块LED灯的开关与周期性闪烁。|
|location|位置信息模块|本模块使用的定位坐标系为WGS-84, 如需转换GCJ-02坐标系，本模块提供了`WGS84ToGCJ02`方法进行经纬度坐标系的转换。|
|logging|日志模块|该模块用于代码日志打印。|
|mpower|低功耗定时唤醒模块|提供定时低功耗唤醒功能，当设备不进行业务处理时，可将设备调整为低功耗模式，当设备唤醒时，可通知用户进行业务处理。|
|quecthing|移远云物联网模块|该模块用于提供移远云物联网模块相关功能，MQTT协议的消息发布与订阅, OTA升级。|
|remote|物联网云兼容模块|该模块作用于云服务与设备直接消息交互的中间件。|
|temp_humidity_sensor|温湿度传感器模块|该模块用于读取温湿度传感器数据。|
