# 串口通信模块 API 参考手册

中文 | [English](../en/serial_API_Reference.md)

## 简介

> 该模块用于串口通信（阻塞、非阻塞模式读）。

## API 说明

### Serial

> 初始化。

```python
from serial import Serial

# 以下示例参数与默认参数一致
serial = Serial(
    port=2,  # 移远模组UART编号
    baudrate=115200,  # 波特率
    bytesize=8,  # 数据位[5 ~ 8]
    parity=0,  # 奇偶校验(0 – NONE，1 – EVEN，2 – ODD)
    stopbits=1,   # 停止位[1 ~ 2]
    flowctl=0  # 硬件控制流(0 – FC_NONE， 1 – FC_HW)
)
```

### Serial.write

> 串口写。

```python
# 行为与`machine.UART.write`行为一致。
serial.write(b'hello world!')
```

### Serial.read

> 串口读。

```python
# 非阻塞模式读，行为与`machine.UART.read`一致
r_data = serial.read(1024)  # timeout关键字参数默认为0

# 阻塞读。直到读取1024字节。（若未读取满指定字节，则永远阻塞等待。）
r_data = serial.read(1024, timeout=-1)

# 阻塞读。读满指定字节则立刻返回。（超时timeout(ms)后仍未读满指定字节，则返回实际读取字节。）
r_data = serial.read(1024, timeout=1000)
```
