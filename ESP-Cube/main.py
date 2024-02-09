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
    Tmp = round(2*(wert1["Tmp"]+wert2["Tmp"]+wert3["Tmp"])/3, 0)/2 # um auf 0,5 zu Runden
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
        ausgabewert = None# nichts konkretes = oben
    
    database = helper.load_data("RotInfo.dat")
    if database["Zustand"] == ausgabewert:
        if ausgabewert == "1": # damit die Temperatur immer übertragen wird in Zustand 1
            if Tmp != database["Temperatur"]: # außer die Temperatur hat sich nicht signifikant geändert
                database["Zustand"] = ausgabewert
                database["Temperatur"] = Tmp
                helper.save_data(database, "RotInfo.dat")
                return ausgabewert, Tmp
    else:
        database["Zustand"] = ausgabewert
        database["Temperatur"] = Tmp
        helper.save_data(database, "RotInfo.dat")
        return ausgabewert, Tmp


Antwort = getAnswer() # Antwort = Rotatioszustand
print(Antwort)
if Antwort != None:
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
        if Antwort[0] == "6":
            Zeit = 600000 # = 600s = 10 min
            helper.blink(cnt = 10)
            Pin(2, Pin.OUT).off()
        else:
            Zeit = 4000
        deepsleep(Zeit)
deepsleep(2000)
