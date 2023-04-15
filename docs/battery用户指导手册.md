# 电池功能模块 用户指导手册

## 简介

> 该模块用于查询当前设备的电池电量与电压, 设备的充电状态。

## API说明

### 实例化对象

**示例:**

```python
from battery import Battery

adc_args = (adc_num, adc_period, factor)
chrg_gpion = 0
stdby_gpion = 1

battery = Battery(adc_args=adc_args, chrg_gpion=chrg_gpion, stdby_gpion=stdby_gpion)
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|adc_args|tuple|元素1: [ADC通道](https://python.quectel.com/wiki/#/zh-cn/api/QuecPythonClasslib?id=%e8%af%bb%e5%8f%96%e9%80%9a%e9%81%93%e7%94%b5%e5%8e%8b%e5%80%bc), 元素2: ADC循环读取次数, 元素3: 计算系数, 可选|
|chrg_gpion|int|CHRG （引脚 1）：漏极开路输出的充电状态指示端。可选|
|stdby_gpion|int|STDBY （引脚 5）：电池充电完成指示端。可选|

### set_charge_callback

> 充电事件回调函数

**示例:**

```python
def charge_callback(charge_status):
    print(charge_status)

res = battery.set_charge_callback(charge_callback)
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|charge_callback|function|充电事件回调函数, 回调函数参数为设备充电状态: 0-未充电;1-充电中;2-充电完成|

**返回值:**

|数据类型|说明|
|:---|---|
|bool|`True`成功, `False`失败|

### set_temp

> 设置当前设备所处工作环境温度, 用于计算设备电池电量

**示例:**

```python
res = battery.set_temp(20)
```

**参数:**

|参数|类型|说明|
|:---|---|---|
|temp|int/float|温度值, 单位:摄氏度 |

**返回值:**

|数据类型|说明|
|:---|---|
|bool|`True`成功, `False`失败|

### voltage

> 查询电池电压

**示例:**

```python
battery.voltage
# 523
```

**返回值:**

|数据类型|说明|
|:---|---|
|int|电池电压, 单位mV。|

### energy

> 查询电池电量

**示例:**

```python
res = battery.energy
# 100
```

**返回值:**

|数据类型|说明|
|:---|---|
|int|电池电量百分比, 0~100。|

### charge_status

> 查询充电状态

**示例:**

```python
battery.charge_status
# 1
```

**返回值:**

|数据类型|说明|
|:---|---|
|int|0-未充电<br>1-充电中<br>2-充电完成|

## 使用示例

```python
from battery import Battery

# 实例化对象
adc_args = (adc_num, adc_period, factor)
chrg_gpion = 0
stdby_gpion = 1
battery = Battery(adc_args=adc_args, chrg_gpion=chrg_gpion, stdby_gpion=stdby_gpion)

def charge_callback(charge_status):
    print(charge_status)

# 设置充电状态回调函数
battery.set_charge_callback(charge_callback)
# True

# 设置当前设备温度
temp = 30
battery.set_temp(temp)
# True

# 获取当前电池电压
battery.voltage
# 3000

# 获取当前电池电量
battery.energy
# 100

# 获取当前充电状态
battery.charge_status
# 1

```
