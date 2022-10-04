from machine import Pin
import time

led = Pin(2, Pin.OUT)
"""
while True:
    led.on()
    print("LED OFF")
    time.sleep(1)
    led.off()
    print("LED ON")
    time.sleep(1)
"""
for i in range(200):
    led.off()
    print("LED ist jetzt an LOL und zwar lang")
    time.sleep(1)
    led.on()
    print("kurz")
    time.sleep(0.1)
    led.off()
    print("kurz")
    time.sleep(0.25)
    led.on()
    print("kurz")
    time.sleep(0.1)
    led.off()
    print("kurz")
    time.sleep(0.05)
    led.on()
    print("kurz")
    time.sleep(0.1)