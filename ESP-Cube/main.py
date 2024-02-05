import time
from machine import SoftI2C
from machine import Pin, deepsleep
from machine import sleep
import mpu6050
import urequests

print("wait for start-interrupt")
time.sleep(2)

i2c = SoftI2C( scl=Pin(22), sda=Pin(21), freq=100000)     #initializing the I2C method for ESP32
#i2c = I2C(scl=Pin(5), sda=Pin(4))       #initializing the I2C method for ESP8266
mpu= mpu6050.accel(i2c)

p2 = Pin(2,Pin.OUT)
p2.on()

ausgabewortalt = ""

def getAnswer():
    global ausgabewortalt
    wert1 = mpu.get_values()
    wert2 = mpu.get_values()
    wert3 = mpu.get_values()
    x = round((wert1["AcX"]+wert2["AcX"]+wert3["AcX"])/16384/3, 2)
    y = round((wert1["AcY"]+wert2["AcY"]+wert3["AcY"])/16384/3, 2)
    z = round((wert1["AcZ"]+wert2["AcZ"]+wert3["AcZ"])/16384/3, 2)
    #print(str(x) + "  " + str(y) + " " + str(z))
    
    if x >= 0.7 and -0.3 < y < 0.3 and -0.3 < z < 0.3:
        ausgabewort = "1" # oben = oben
    elif x <= -0.7 and -0.3 < y < 0.3 and -0.3 < z < 0.3:
        ausgabewort = "6"# unten = oben
    elif z <= -0.7 and -0.3 < y < 0.3 and -0.3 < x < 0.3:
        ausgabewort = "4"# links = oben
    elif z >= 0.7 and -0.3 < y < 0.3 and -0.3 < x < 0.3:
        ausgabewort = "3"# drei = oben
    elif y <= -0.7 and -0.3 < x < 0.3 and -0.3 < z < 0.3:
        ausgabewort = "5"# hinten = oben
    elif y >= 0.7 and -0.3 < x < 0.3 and -0.3 < z < 0.3:
        ausgabewort = "2"# vorne = oben
    else:
        ausgabewort = "0"# nicht konkretes = oben
    
    if ausgabewortalt == ausgabewort:
        pass
    else:
        ausgabewortalt = ausgabewort
        return ausgabewort

Antwort = getAnswer() # Antwort = Rotatioszustand
print(Antwort)
url = "http://dog42.de:8000/stat/" + str(Antwort)
urequests.post(url)

p2.off()
deepsleep(2000)
