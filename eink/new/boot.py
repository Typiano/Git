# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

def do_connect():
    import network
    from config import ssid, pw
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, pw)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    return True

do_connect()
