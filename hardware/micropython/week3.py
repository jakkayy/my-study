from machine import Pin, PWM, ADC, I2C
from time import sleep
import ssd1306

red = PWM(Pin(42, Pin.OUT))
yellow = PWM(Pin(41, Pin.OUT))
green = PWM(Pin(40, Pin.OUT))
sw = Pin(2, Pin.IN, Pin.PULL_UP)
i2c = I2C(0, scl=Pin(47), sda=Pin(48))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

ldr = ADC(Pin(4))
ldr.atten(ADC.ATTN_11DB)

def clearLED():
    red.duty(0)
    yellow.duty(0)
    green.duty(0)
    display.fill(0)


#for i in range(50):
    #display.pixel(10, i)
    #display.show()
        
    #for t1 in range(5):
       # display.pixel(0, 0, t1)
       # display.pixel(0, 25, t1)
       # display.show()

# display.text('Light Level:', 0, 0)
# display.show()

while True:
    clearLED()
    print(ldr.read())
    display.text('Light Level:', 0, 0)
    if ldr.read() <= 1365:
        red.duty(1023)
        if sw.value() == 0:
            display.text('Pressed', 0, 30)
            
    elif 1365 < ldr.read() <= 2730:
        yellow.duty(1023)
        if sw.value() == 0:
            display.text('Pressed', 0, 30)
            
    elif 2730 < ldr.read():
        green.duty(1023)
        if sw.value() == 0:
            display.text('Pressed', 0, 30)
            
    power = int(ldr.read()/40.95)
    #display.hline(0,15,100,0)
    display.rect(0,15,100,5,1)
    display.fill_rect(0,15,100-power,5,1)
    display.text(str(100-int(ldr.read()/40.95)),100,15)
    display.show()
    
    sleep(0.05)