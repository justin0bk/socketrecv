import sys
import socket
import RPi.GPIO as GPIO
import time

def get_ip_address():
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


def re_port(soc, host):
    new_port = int(input('Insert another port number'))
    try:
        soc.bind((host, new_port))
    except socket.error:
        print('There is still a problem connecting to the port')
        re_port(soc, host)

def initialize_exp():

    global client

    GPIO.output(desig_onoff, 1)

    mouse_init = 0
    mouselist = []
    while mouse_init == 0:
        msg = client.recv(1028).decode()
        print(msg)
        if msg == 'CountDone':
            mouse_init = 1
        else:
            mouselist.append(msg)
            
        time.sleep(0.05)

    print('init Done')

    hist = {k: 0 for k in mouselist}
    p = {}
    p2 = {}
        
    pin = {}

    msg = client.recv(1028).decode()
    if msg == 'cl':
        closed_loop(10, 5)
    elif msg == 'ol':
        hi = client.recv(1028).decode()
        lo = client.recv(1028).decode()
        dur = client.recv(1028).decode()
        print(hi)
        print(lo)
        print(dur)
        open_loop(hi,lo,dur)
    elif msg == 'nn':
        return
    return


def closed_loop(hi, lo):

    global client

    pins = [15, 16, 18, 22, 29, 31, 32, 33]
    pin_num = 0

    for mouse in mouselist:
        pin[mouse] = pins[pin_num:pin_num+2]
        pin_num += 2
        
    for mouse in mouselist:
        for pin in pin[mouse]:
            GPIO.setup(pin, GPIO.OUT, initial = 0)

    onOff = {k: 0 for k in mouselist}
    terminate = 0
    freq = int(1000/hi+lo)
    dutcy = int(hi/(hi+lo))*100

    while terminate == 0:
        msg = client.recv(1028).decode()
        print(msg)
        if msg == 'STOP':
            GPIO.output(36, 0)
            onOff = 2
            terminate = 1
        else:
            mouse = msg[0:-1]
            onOff[mouse] = int(msg[-1])
            # print(onOff)
            if len(mouse) < 4:
                read_onOff(mouse, onOff[mouse], freq, dutcy)


def open_loop(hi, lo, dur):

    global client
    
    freq = int(1000/hi+lo)
    dutcy = int(hi/(hi+lo))*100
    puldur = dur

    GPIO.setup(desig_laser, GPIO.OUT, initial = 0)
    switch = 1

    while switch == 1:
        run_signal = client.recv(1028).decode()
        if run_signal == 'STOP':
            switch = 0
            GPIO.output(36, 0)
        elif run_signal == 'r':
            p = GPIO.PWM(desig_laser, freq)
            p.start(dutcy)
            time.sleep(puldur*1000)
            p.stop()

    
def read_onOff(mouse, number, freq, dutcy):
    if hist[mouse] == number:
        return
    else:
        if number == 2:
            p[mouse] = GPIO.PWM(pin[mouse][0],freq)
            p2[mouse] = GPIO.PWM(pin[mouse][1],freq)
            p[mouse].start(dutcy)
            p2[mouse].start(dutcy)
            hist[mouse] = number
        elif number == 1:
            p[mouse] = GPIO.PWM(pin[mouse][0],freq)
            p2[mouse] = GPIO.PWM(pin[mouse][1],freq)
            p2[mouse].start(dutcy)
            hist[mouse] = number                
        else:
            p[mouse].stop()
            hist[mouse] = number

def start_cycle():
    
    global client

    while True:
        msg = client.recv(1028).decode()
        if msg == 'START':
            print('START')
            initialize_exp()
        if msg == 'END':
            return


onOff = 0
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

desig_laser = 37
desig_onoff = 36
GPIO.setup(desig_onoff, GPIO.OUT, initial = 0)

server  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("make sure you change the host IP appropriately - remove lock")
lock

host = get_ip_address()
port = 5010

try:
    server.bind((host,port))
except socket.error:
    print('Port' + str(port) + ' is occupied')
    re_port(server, host)

server.listen(5)
client, address = server.accept()
print('Client found:', address)

start_cycle()







        
    
    

        
        

