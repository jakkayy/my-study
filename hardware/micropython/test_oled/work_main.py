from machine import Pin, PWM, ADC, I2C
from time import sleep
import ssd1306

red = PWM(Pin(42, Pin.OUT))
yellow = PWM(Pin(41, Pin.OUT))
green = PWM(Pin(40, Pin.OUT))
sw = Pin(2, Pin.IN, Pin.PULL_UP)
i2c = I2C(0, scl=Pin(47), sda=Pin(48))
ldr = ADC(Pin(4))
ldr.atten(ADC.ATTN_11DB)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

def clearLED():
    red.duty(0)
    yellow.duty(0)
    green.duty(0)

def block_power(display):
    for i in range(25):
        display.pixel(0, -i, 10)
        display.pixel(0, -i, -10)
        display.show()
        
    for t1 in range(5):
        display.pixel(0, 25, t1)
        display.pixel(0, 25, -t1)
        display.pixel(0, -25, t1)
        display.pixel(0, -25, -t1)
        display.show()
    
    for j in range(1,26):
        display.pixel(0, j, 5)
        display.pixel(0, j, -5)
        display.show()


        
display.text('Light Level:', -25, -10)
block_power(display)
display.show()

while True:
    clearLED()
    print(ldr.read())
    
    number = int(ldr.read()/41)
    for m in range(-25, (number/2)-25):
        for n in range(10):
            display.pixel(0, m, n-5)
            display.show()
            
    display.text(str(number), 30, 0)
    display.show()
    if sw.value() == 0:
        sleep(1)
        if sw.value() == 0:
            display.text('Pressed', 0, -20)
            display.show()
    if ldr.read() <= 1365:
        red.duty(1023)
    elif 1365 < ldr.read() <= 2730:
        yellow.duty(1023)
    elif 2730 < ldr.read() <= 4095:
        green.duty(1023)
        
    sleep(0.05)