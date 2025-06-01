from machine import Pin, time_pulse_us, I2C, PWM
import time
import ssd1306
import network
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS,
    TOPIC_PREFIX
)
from umqtt.simple import MQTTClient

TOPIC_DIST_HUMAN_IN = f'{TOPIC_PREFIX}/dist/humanin'
TOPIC_DIST_HUMAN_OUT = f'{TOPIC_PREFIX}/dist/humanout'
TOPIC_ALLOW_HUMAN = f'{TOPIC_PREFIX}/allow/human'
TOPIC_DIST_CAR_IN = f'{TOPIC_PREFIX}/dist/carin'
TOPIC_DIST_CAR_OUT = f'{TOPIC_PREFIX}/dist/carout'
TOPIC_ALLOW_CAR = f'{TOPIC_PREFIX}/allow/car'

def connect_wifi():
    mac = ':'.join(f'{b:02X}' for b in wifi.config('mac'))
    print(f'WiFi MAC address is {mac}')
    wifi.active(True)
    print(f'Connecting to WiFi {WIFI_SSID}.')
    wifi.connect(WIFI_SSID, WIFI_PASS)
    while not wifi.isconnected():
        print('.', end='')
        time.sleep(0.5)
    print('\nWiFi connected.')


def connect_mqtt():
    print(f'Connecting to MQTT broker at {MQTT_BROKER}.')
    mqtt.connect()
    mqtt.set_callback(mqtt_callback)
    mqtt.subscribe(TOPIC_DIST_HUMAN_IN)
    mqtt.subscribe(TOPIC_DIST_HUMAN_OUT)
#     mqtt.subscribe(TOPIC_RED_HUMAN)
#     mqtt.subscribe(TOPIC_YELLOW_HUMAN)
#     mqtt.subscribe(TOPIC_GREEN_HUMAN)
    mqtt.subscribe(TOPIC_ALLOW_HUMAN)

    print('MQTT broker connected.')

def measure_distance():
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()

    duration = time_pulse_us(echo, 1, 30000)
    distance = (duration * 0.0343) / 2 
    return distance

def clear():
    red.value(0)
    yellow.value(0)
    green.value(0)
    display.fill(0)
    display.show()
    
def set_servo_angle(angle):
    minDuty = 2000 
    maxDuty = 8000
    duty = minDuty + (angle / 180) * (maxDuty - minDuty)
    servo.duty_u16(int(duty))
    
def mqtt_callback(topic, payload):
    global dist
    if topic.decode() == TOPIC_DIST_HUMAN_OUT:
        print(payload.decode())
        try:
            clear()
            set_servo_angle(15)
            green.value(1)
            display.text("GO", 50, 25)
            display.show()
        except ValueError:
            pass
    elif dist > 10:
        if topic.decode() == TOPIC_DIST_HUMAN_IN:
            print(payload.decode())
            try:
                clear()
#                 yellow.value(1)
#                 time.sleep(1)
#                 yellow.value(0)
                red.value(1)
                set_servo_angle(110)
                display.text("STOP", 50, 25)
                display.show()

            except ValueError:
                pass
    elif dist <= 10:
        if topic.decode() == TOPIC_DIST_HUMAN_IN:
            print(payload.decode())
            try:
                clear()
                green.value(1)
                display.text("GO", 50, 25)
                display.show()
            except ValueError:
                pass
    elif topic.decode() == TOPIC_DIST_HUMAN_IN:
        print(payload.decode())
        try:
            clear()
            if dist > 10:
#                 yellow.value(1)
#                 time.sleep(1)
#                 yellow.value(0)
                red.value(1)
                set_servo_angle(110)
                display.text("STOP", 50, 25)
                display.show()
#             elif dist <= 10:
                
        except ValueError:
            pass

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
wifi = network.WLAN(network.STA_IF)
mqtt = MQTTClient(client_id='',
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)

connect_wifi()
connect_mqtt()
r = 0    
count = 0
while True:
    dist = measure_distance()
    mqtt.check_msg()   
    print(f"Distance: {dist:.2f} cm")
    
    if dist <= 10:
        mqtt.publish(TOPIC_DIST_CAR_IN, str(dist))
        
    else:
        mqtt.publish(TOPIC_DIST_CAR_OUT, str(dist))
        
    time.sleep(1)
    