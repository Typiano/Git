from machine import Pin
from time import sleep

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('ERROR303', 'foobar404')
        # wlan.connect("KH Gastzugang", "kanzleihofmann2015")
        while not wlan.isconnected():
            pass
    else:
        print("wlan already is connected")
    print('network config:', wlan.ifconfig(), "\n\n")

do_connect()

def http_post(url, daten):
    
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('POST /%s HTTP/1.0\r\nHost: %s\r\n' % (path, host), 'utf8'))
    s.send(bytes('content-type: text/text\r\n', 'utf8'))
    s.send(bytes('content-length: %s\r\n\r\n' % len(daten), 'utf8'))
    s.send(bytes('%s\r\n'% daten, 'utf8'))
    
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

#url = "https://webhook.site/9ed8419d-f4fd-4090-947e-f964ef9dfe14"
#http_post(url, "Das ist ein Test")
