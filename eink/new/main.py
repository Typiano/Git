from machine import Pin, SoftSPI, deepsleep
from time import sleep_ms
import epaper4in2
import urequests
from helper import *

p2 =Pin(2,Pin.OUT)
p2.on()
print("wait for start-interrupt")
sleep_ms(3000)


# SPIV on ESP32

miso = Pin(12) # NOT USED
mosi = Pin(27) # DIN
sck = Pin(25) #CLK
cs = Pin(32) #Chipselect
dc = Pin(12) # Data/Command
rst = Pin(4) #RST
busy = Pin(0) #Busy
spi = SoftSPI(baudrate=20000000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)

e = epaper4in2.EPD(spi, cs, dc, rst, busy)
e.init()

w = 400
h = 300
x = 0
y = 0


# use a frame buffer
# 400 * 300 / 8 = 15000 - thats a lot of pixels
import framebuf
buf = bytearray(w * h // 8)
fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
black = 0
white = 1
fb.fill(white)




if do_connect():
    #textdata = http_get("http://192.168.0.131/txt/5", 8000)
    try:
        resp = urequests.get("http://192.168.1.23:8000/statustext", headers={'Content-Type':'text/json'})
    except:
        print("cant connect to server")
    else:
        print("NEW DATA:", resp.json())
        data=load_data()
        if  data["status"] != resp.json()["status"]:
            blink()
            data = resp.json()
            print("status changed to: " + str(data["status"]))
            e. init()
            fb.fill(white)
            e.set_display_frame(buf,buf)
            fb.text(str(resp.json()["message"]),0,0,black)
            text_wrap(fb,str(resp.json()["text"]),0,20,black, w=400, h=40)
            e.set_display_frame(buf,None)
            e.show_display_frame()
            save_data(data)
            sleep_ms(15000)
            e.sleep()
print('go to deep sleep')
p2.off()
#sleep_ms(10000)
deepsleep(60000)
