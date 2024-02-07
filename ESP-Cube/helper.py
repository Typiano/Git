import ujson
from machine import Pin
from time import sleep_ms

def blink(pin=2, cnt=3):
    p =Pin(pin,Pin.OUT)
    for i in range(cnt):
        p.off()
        sleep_ms(200)
        p.on()
        sleep_ms(200)

def save_data(data, name):
    f=open(name,"w") # opens a file for writing.
    f.write(ujson.dumps(data))
    f.close()

def load_data(name):
    f=open(name,"r")
    # print(f.read())
    data = ujson.load(f)
    # print("OLD DATA:", data)
    f.close()
    return data

def text_wrap(fb,str,x=0,y=0,color=0,w=80,h=10,border=None):
	# optional box border
	if border is not None:
		fb.rect(x, y, w, h, border)
	cols = w // 8
	# for each row
	j = 0
	for i in range(0, len(str), cols):
		# draw as many chars fit on the line
		fb.text(str[i:i+cols], x, y + j, color)
		j += 8
		# dont overflow text outside the box
		if j >= h:
			break
		
def do_connect():
    import network
    from config import ssid, pw
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        wlan.active(True)
        print('connecting to network...')
        wlan.connect(ssid, pw)
        #wlan.connect("KH Gastzugang", "kanzleihofmann2015")
        while not wlan.isconnected():
            pass
    else:
        print("wlan already is connected")
    # print('network config:', wlan.ifconfig(), "\n\n")
    # return True
