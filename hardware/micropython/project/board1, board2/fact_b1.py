from machine import Pin, ADC, I2C, time_pulse_us
import ssd1306
import time
import network
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS,
    TOPIC_PREFIX
)
from umqtt.simple import MQTTClient

TOPIC_DIST_HUMAN_IN = f'{TOPIC_PREFIX}/dist/humanin'
TOPIC_DIST_HUMAN_OUT = f'{TOPIC_PREFIX}/dist/humanout'
TOPIC_RED_HUMAN = f'{TOPIC_PREFIX}/red/human'
TOPIC_YELLOW_HUMAN = f'{TOPIC_PREFIX}/yellow/human'
TOPIC_GREEN_HUMAN = f'{TOPIC_PREFIX}/green/human'
TOPIC_ALLOW_HUMAN = f'{TOPIC_PREFIX}/allow/human'
TOPIC_ALLOW_CAR = f'{TOPIC_PREFIX}/allow/car'
TOPIC_DIST_CAR_IN = f'{TOPIC_PREFIX}/dist/carin'
TOPIC_DIST_CAR_OUT = f'{TOPIC_PREFIX}/dist/carout'

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
    mqtt.subscribe(TOPIC_DIST_CAR_IN)
    mqtt.subscribe(TOPIC_DIST_CAR_OUT)
    mqtt.subscribe(TOPIC_ALLOW_CAR)
#     mqtt.subscribe(TOPIC_RED_CAR)
#     mqtt.subscribe(TOPIC_YELLOW_CAR)
#     mqtt.subscribe(TOPIC_GREEN_CAR)
    
    print('MQTT broker connected.')

def clear():
    red.value(0)
    yellow.value(0)
    green.value(0)
    display.fill(0)
    

def measure_distance():
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()

    duration = time_pulse_us(echo, 1, 30000)
    distance = (duration * 0.0343) / 2 
    return distance

def mqtt_callback(topic, payload):
    global dist, key
    if topic.decode() == TOPIC_DIST_CAR_OUT:
        print(payload.decode())
        clear()
        try:
            if key == 7:
                display.text("STOP", 50, 25)
                red.value(1)
            elif key == 1:
                red.value(1)
                display.text("You want cross?", 0, 25)
                if key == 0:
                    clear()
                    display.text("GO", 50, 25)
                    green.value(1)
                    buzzer.value(1)
                    time.sleep_ms(500)  
                    buzzer.value(0)
                else:
                    red.value(1)
                    display.text("You want cross?", 0, 25)
            elif key == 0:
                display.text("GO", 50, 25)
                green.value(1)
            display.show()
        except ValueError:
                pass
    if topic.decode() == TOPIC_DIST_CAR_IN:
        print(payload.decode())
        try:
            clear()
            if key == 7:
                display.text("STOP", 50, 25)
                red.value(1)
            elif key == 1:
                red.value(1)
                display.text("You want cross?", 0, 25)
                if sw.value() == 0:
                    clear()
                    key = 0
                    display.text("wait", 50, 25)
                    red.value(1)
            elif key == 0:
                display.text("wait", 50, 25)
                red.value(1)
            display.show()
        except ValueError:
            pass

#setup
RED_GPIO = 42
YELLOW_GPIO = 41
GREEN_GPIO = 40
TRIG_PIN = 5
ECHO_PIN = 6
sw = Pin(2, Pin.IN, Pin.PULL_UP)
red = Pin(RED_GPIO, Pin.OUT)
yellow = Pin(YELLOW_GPIO, Pin.OUT)
green = Pin(GREEN_GPIO, Pin.OUT)
i2c = I2C(0, scl=Pin(47), sda=Pin(48))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
buzzer = Pin(7, Pin.OUT)
wifi = network.WLAN(network.STA_IF)
mqtt = MQTTClient(client_id='',
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)

connect_wifi()
connect_mqtt()


key = 7
while True:
    dist = measure_distance()
    mqtt.check_msg()
    print(f"Distance: {dist:.2f} cm")
    print(key)
    
    if dist <= 10:
        mqtt.publish(TOPIC_DIST_HUMAN_IN, str(dist))
        if sw.value() == 0:
            key = 0
        else:
            pass
    else:
        mqtt.publish(TOPIC_DIST_HUMAN_OUT, str(dist))
        if sw.value() == 0:
            key = 1
        else:
            key = 1

    time.sleep(1)
