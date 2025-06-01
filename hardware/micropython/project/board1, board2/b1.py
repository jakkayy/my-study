from machine import Pin, time_pulse_us, I2C
import time
import ssd1306

TRIG_PIN = 5
ECHO_PIN = 6
sw = Pin(2, Pin.IN, Pin.PULL_UP)
red = Pin(42, Pin.OUT)
yellow = Pin(41, Pin.OUT)
green = Pin(40, Pin.OUT)
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
i2c = I2C(0, scl=Pin(47), sda=Pin(48))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
buzzer = Pin(7, Pin.OUT)

    
def measure_distance():
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()

    duration = time_pulse_us(echo, 1, 30000)
    distance = (duration * 0.0343) / 2 
    return distance

def clear_LED():
    red.value(0)
    yellow.value(0)
    green.value(0)
    display.fill(0)
    
count = 5
traf = 7
while True:
    dist = measure_distance()
    buzzer.value(0)
    clear_LED()
    print(f"Distance: {dist:.2f} cm")
    if dist <= 10:
        traf = 0   
        if count != 0:
            red.value(1)
            display.text("you want cross?",0 ,10)
            display.text("Press the button",0 ,25) 
            if sw.value() == 0 :
                red.value(0)
                count = 0
                display.fill(0)
                display.text("GO", 50, 25)
                green.value(1)
                buzzer.value(1)
                time.sleep_ms(500)  # เล่นเสียงตามระยะเวลา
                buzzer.value(0)
            else:
                pass
        elif count == 0:
            green.value(1)
            display.fill(0)
            display.text("GO", 50, 25)
            
    else:
        count = 2
        buzzer.value(0)
        display.text("STOP", 50, 25)
        if traf == 7:
            red.value(1)
            traf = 0
        elif traf == 0:
            red.value(0)
            green.value(0)
            yellow.value(1)
            traf += 1
        else:
            yellow.value(0)
            red.value(1)
    time.sleep(1)
    display.show()

    