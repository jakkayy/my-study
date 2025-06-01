from machine import Pin, time_pulse_us, I2C, PWM
import time
import ssd1306
# import network
# from config import (
#     WIFI_SSID, WIFI_PASS,
#     MQTT_BROKER, MQTT_USER, MQTT_PASS,
#     TOPIC_PREFIX
# )
# from umqtt.simple import MQTTClient

TRIG_PIN = 5
ECHO_PIN = 6
red = Pin(42, Pin.OUT)
yellow = Pin(41, Pin.OUT)
green = Pin(40, Pin.OUT)
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
i2c = I2C(0, scl=Pin(47), sda=Pin(48))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
servo = PWM(Pin(18), freq=50)

def set_servo_angle(angle):
    minDuty = 2000 
    maxDuty = 8000
    duty = minDuty + (angle / 180) * (maxDuty - minDuty)
    servo.duty_u16(int(duty)) 
    
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
    
count = 0
while True:
    dist = measure_distance()
    clear_LED()     
    print(f"Distance: {dist:.2f} cm")
    if dist < 0 :
        pass
    elif dist > 10:
        set_servo_angle(110)
        green.value(1)
        count = 0
        display.text('GO',50, 25)
    else:
        set_servo_angle(15)
        display.text('STOP', 50, 25)
        if count == 0:
            green.value(0)
            yellow.value(1)
            count += 1
        else:
            yellow.value(0)
            red.value(1)
    display.show()
    time.sleep(1)