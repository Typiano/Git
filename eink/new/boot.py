# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('ERROR303', 'foobar404')
        #wlan.connect("KH Gastzugang", "kanzleihofmann2015")
        while not wlan.isconnected():
            pass
    else:
        print("wlan already is connected")
    print('network config:', wlan.ifconfig(), "\n\n")

#do_connect()
