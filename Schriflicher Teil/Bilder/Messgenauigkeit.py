import time
from machine import SoftI2C
from machine import Pin, deepsleep
import mpu6050

i2c = SoftI2C( scl=Pin(22), sda=Pin(21), freq=100000)     #initializing the I2C method for ESP32
mpu= mpu6050.accel(i2c)

Liste = []

for i in range(1000):
    xwert = mpu.get_values()["AcX"]
    wert = xwert/16384
    Liste.append(wert)

print(Liste)