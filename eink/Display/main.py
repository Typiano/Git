import machine
from time import sleep_ms
import time
import epaper4in2
import urequests
import helper
from config import Link

print("wait for start-interrupt")
time.sleep(1)

def NeuesBild(datenlage, tempdatenlage):
    # SPIV on ESP32
    miso = machine.Pin(12) # NOT USED
    mosi = machine.Pin(27) # DIN
    sck = machine.Pin(25) #CLK
    cs = machine.Pin(32) #Chipselect
    dc = machine.Pin(12) # Data/Command
    rst = machine.Pin(4) #RST
    busy = machine.Pin(0) #Busy
    spi = machine.SoftSPI(baudrate=20000000, polarity=0, phase=0, sck=sck, miso=miso, mosi=mosi)

    e = epaper4in2.EPD(spi, cs, dc, rst, busy)
    e.init()

    w = 400
    h = 300
    x = 0
    y = 0
    # use a frame buffer
    # 400 * 300 / 8 = 15000 - thats a lot of pixels
    if datenlage["status"] != 2:
        rtc = machine.RTC().datetime()
        import framebuf
        buf = bytearray(w * h // 8)
        fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
        black = 0
        white = 1
        fb.fill(white)
        e.set_display_frame(buf,buf)# Hinergrund wird weiß gefärbt
        if datenlage["status"] == 1:# die Wetter Seite
            t1 = str(tempdatenlage["Temperatur"]) + " Grad Celsius"
            t2 = "Es ist exakt um " + str(rtc[4]) + ":" + str(rtc[5]) + " Uhr."
            fb.text(t1, round(w/2 - len(t1)*4), 20, black)
            fb.text(t2, round(w/2 - len(t2)*4), 40, black)
            e.set_display_frame(buf,None)# hier drüber wird schwarz geschrieben
            fb.fill(white)
            tt1 = tempdatenlage["TempZusatz"]
            helper.text_wrap(fb,str(tt1),round(w/2-helper.hufuregel(tt1)),175,black, w=300, h=100)
            e.set_display_frame(None, buf)# hier drüber wird rot geschrieben
        elif datenlage["status"] == 6:
            fb.fill(black)
            taus1 = datenlage["text"]
            helper.text_wrap(fb,str(taus1),round(w/2-helper.hufuregel(taus1)),150, white, w=300, h=100)
            e.set_display_frame(buf, None)# hier drüber wird weiß auf schwarz geschrieben
            fb.fill(white)
            e.set_display_frame(None,buf)# hier drüber wird rot geschrieben
        else: 
            tnorm1, tnorm2 = datenlage["text"].split("SPLIT", 1)
            tnormtemp = str(tempdatenlage["Temperatur"]) + " Grad Celsius"
            tnormuhr = str(rtc[4]) + ":" + str(rtc[5]) + " Uhr"
            helper.text_wrap(fb,str(tnorm1),round(w/2-helper.hufuregel(tnorm1)),50, black, w=300, h=100)
            helper.text_wrap(fb,str(tnormuhr),round(w-helper.hufuregel(tnormuhr)*2-10),10, black, w=300, h=100)
            helper.text_wrap(fb,str(tnormtemp),10 ,10, black, w=300, h=100)
            e.set_display_frame(buf,None)# hier drüber wird schwarz geschrieben
            fb.fill(white)
            fb.rect(round(w/2-helper.hufuregel(tnorm2)-4), 170, helper.hufuregel(tnorm2)*2+8, 18, black)
            helper.text_wrap(fb,str(tnorm2),round(w/2-helper.hufuregel(tnorm2)),175, black, w=300, h=100)
            e.set_display_frame(None, buf)# hier drüber wird rot geschrieben
        e.show_display_frame()
        e.sleep()
    else:
        import framebuf
        from htwk40x30 import htwk40x30
        buf = bytearray(w * h // 8)
        fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
        black = 0
        white = 1
        fb.fill(white)
        e.set_display_frame(buf, buf)
        fb.blit(framebuf.FrameBuffer(htwk40x30, 40, 30, framebuf.MONO_HLSB), 10,10, black)
        e.set_display_frame(buf, None)# hier drüber wird rot geschrieben
        e.show_display_frame()
        del htwk40x30
        e.sleep()
                
        pass # hier das Bild einfügen...
    """
    import framebuf
    buf = bytearray(w * h // 8)
    fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
    black = 0
    white = 1
    fb.fill(white)
    fb.text('Hello World',30,10,black)
    fb.pixel(30, 10, black)
    fb.hline(30, 30, 10, black)
    fb.vline(30, 50, 10, black)
    fb.line(30, 70, 40, 80, black)
    fb.rect(30, 90, 10, 10, black)
    fb.fill_rect(30, 110, 10, 10, black)
    for row in range(0,37):
        fb.text(str(row),0,row*8,black)
    fb.text('Line 36',0,288,black)
    e.set_display_frame(buf, buf)
    e.show_display_frame()
    #e.sleep()
    
    import framebuf
    buf = bytearray(w * h // 8)
    fb = framebuf.FrameBuffer(buf, w, h, framebuf.MONO_HLSB)
    black = 0
    white = 1
    fb.fill(white)
    
    #e.init()
    fb.fill(white)
    e.set_display_frame(buf,buf) # für Hintergrund?
    #fb.text(str(resp.json()["message"]),0,0,black)
    helper.text_wrap(fb,str(resp.json()["text"]),20,50,black, w=400, h=30)
    e.set_display_frame(buf,None)
    e.show_display_frame() # für Schrit?
    """
    helper.save_data(tempdatenlage, "Tempdata.dat")
    helper.save_data(datenlage, "data.dat")
    #time.sleep(15)
    #e.sleep()
    helper.blink(cnt=2)
    machine.Pin(2,machine.Pin.OUT).off()

if helper.do_connect():
    #textdata = http_get("http://192.168.0.131/txt/5", 8000)
    try:
        resp = urequests.get(Link + "/statustext", headers = {'Content-Type':'text/json'})
        datenlage = resp.json()
        print(datenlage)
        tempdatenlage = urequests.get(Link + "/tempstat", headers = {'Content-Type':'text/json'}).json()
    except:
        print("cant connect to server")
    else:
        #print("NEW DATA:", resp.json())
        data=helper.load_data("data.dat")
        tempdata = helper.load_data("Tempdata.dat")
        if  data["status"] != datenlage["status"]:
            data = datenlage
            tempdata = tempdatenlage
            print("status changed to: " + str(data["status"]))
            NeuesBild(datenlage, tempdatenlage)
        elif datenlage["status"] == 1 and tempdata["Temperatur"] != tempdatenlage["Temperatur"]:
            print(tempdata["Temperatur"])
            tempdata = tempdatenlage # falls nur die Temperatur sich ändert
            NeuesBild(datenlage, tempdatenlage)
        elif data["status"] == 6:
            machine.deepsleep(600000)

print('go to deep sleep')

machine.deepsleep(6000)
