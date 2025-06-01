from machine import Pin
from time import sleep

red = Pin(41, Pin.OUT)
yellow = Pin(40, Pin.OUT)
green = Pin(39, Pin.OUT)
sw = Pin(2, Pin.IN, Pin.PULL_UP)
count = 2

while True:
    if sw.value() == 0:
        
        while sw.value() == 0:
            sleep(0.05)
            pass
        
        count += 1
        if count == 3:
            count = 0
        print(count)
    else:
        if count == 1:
            red.value(1)
            yellow.value(0)
            green.value(0)
            
        elif count == 0:
            red.value(0)
            yellow.value(2)
            green.value(0)
            
        else:
            red.value(0)
            yellow.value(0)
            green.value(3)
    