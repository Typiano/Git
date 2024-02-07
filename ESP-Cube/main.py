import time
from machine import SoftI2C
from machine import Pin, deepsleep
import mpu6050
import urequests
import helper

print("wait for start-interrupt")
time.sleep(1)

i2c = SoftI2C( scl=Pin(22), sda=Pin(21), freq=100000)     #initializing the I2C method for ESP32
#i2c = I2C(scl=Pin(5), sda=Pin(4))       #initializing the I2C method for ESP8266
mpu= mpu6050.accel(i2c)

def getAnswer():
#     mpu.get_values() #um die Werte einmal zu erneuern
    wert1 = mpu.get_values()
    wert2 = mpu.get_values()
    wert3 = mpu.get_values()
    x = round((wert1["AcX"]+wert2["AcX"]+wert3["AcX"])/16384/3, 2)
    y = round((wert1["AcY"]+wert2["AcY"]+wert3["AcY"])/16384/3, 2)
    z = round((wert1["AcZ"]+wert2["AcZ"]+wert3["AcZ"])/16384/3, 2)
    Tmp = round((wert1["Tmp"]+wert2["Tmp"]+wert3["Tmp"])/3, 0)
    #print(str(x) + "  " + str(y) + " " + str(z))
    
    if x >= 0.7 and -0.3 < y < 0.3 and -0.3 < z < 0.3:
        ausgabewert = "1" # oben = oben
    elif x <= -0.7 and -0.3 < y < 0.3 and -0.3 < z < 0.3:
        ausgabewert = "6"# unten = oben
    elif z <= -0.7 and -0.3 < y < 0.3 and -0.3 < x < 0.3:
        ausgabewert = "4"# links = oben
    elif z >= 0.7 and -0.3 < y < 0.3 and -0.3 < x < 0.3:
        ausgabewert = "3"# drei = oben
    elif y <= -0.7 and -0.3 < x < 0.3 and -0.3 < z < 0.3:
        ausgabewert = "5"# hinten = oben
    elif y >= 0.7 and -0.3 < x < 0.3 and -0.3 < z < 0.3:
        ausgabewert = "2"# vorne = oben
    else:
        ausgabewert = None# nicht konkretes = oben
    
    database = helper.load_data("RotInfo.dat")
    if database["Zustand"] == ausgabewert:
        pass
    else:
        database["Zustand"] = ausgabewert
        database["Temperatur"] = Tmp
        helper.save_data(database, "RotInfo.dat")
        return ausgabewert, Tmp


Antwort = getAnswer() # Antwort = Rotatioszustand
print(Antwort)
if Antwort[0] != None:
    helper.do_connect()
    import config
    url1 = config.Link + "/stat/" + str(Antwort[0])
    url2 = config.Link + "/tempstat/" + str(Antwort[1])
    urequests.post(url1)
    urequests.post(url2)
    print("Daten verschickt\n")
    helper.blink(cnt = 1)
    Pin(2, Pin.OUT).off()
deepsleep(2000)
