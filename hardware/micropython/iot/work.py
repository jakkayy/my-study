from machine import Pin, ADC, I2C
import ssd1306
import time
import network
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS,
    TOPIC_PREFIX
)
from umqtt.simple import MQTTClient


RED_GPIO = 42
YELLOW_GPIO = 41
GREEN_GPIO = 40
LDR_GPIO = 4
TOPIC_LIGHT = f'{TOPIC_PREFIX}/light'
TOPIC_LED_RED2 = f'{TOPIC_PREFIX}/led/red'
TOPIC_LED_YELLOW2 = f'{TOPIC_PREFIX}/led/yellow'
TOPIC_LED_GREEN2 = f'{TOPIC_PREFIX}/led/green'
TOPIC_DISPLAY_TEXT = f'{TOPIC_PREFIX}/display/text'
TOPIC_SW = f'{TOPIC_PREFIX}/SW'


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
    mqtt.subscribe(TOPIC_LED_RED2)
    mqtt.subscribe(TOPIC_LED_YELLOW2)
    mqtt.subscribe(TOPIC_LED_GREEN2)
    mqtt.subscribe(TOPIC_DISPLAY_TEXT)
    mqtt.subscribe(TOPIC_SW)
    print('MQTT broker connected.')


def mqtt_callback(topic, payload):
    text = []
    if topic.decode() == TOPIC_LED_RED:
        try:
            red.value(int(payload))
        except ValueError:
            pass
    elif topic.decode() == TOPIC_LED_YELLOW:
        try:
            yellow.value(int(payload))
        except ValueError:
            pass
    elif topic.decode() == TOPIC_LED_GREEN:
        try:
            green.value(int(payload))
        except ValueError:
            pass
    elif topic.decode() == TOPIC_DISPLAY_TEXT:
        text.append(payload.decode())
    
    if len(text) == 0:
        pass
    if len(text) > 0:
        display.fill(0)
        display.text(str(text[-1]), 0, 0)         
        display.show()
            


############
# setup
############
sw = Pin(2, Pin.IN, Pin.PULL_UP)
red = Pin(RED_GPIO, Pin.OUT)
yellow = Pin(YELLOW_GPIO, Pin.OUT)
green = Pin(GREEN_GPIO, Pin.OUT)
ldr = ADC(Pin(LDR_GPIO), atten=ADC.ATTN_11DB)
i2c = I2C(0, scl=Pin(47), sda=Pin(48))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
wifi = network.WLAN(network.STA_IF)
mqtt = MQTTClient(client_id='',
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)
connect_wifi()
connect_mqtt()
last_publish = 0


############
# loop
############
key = 4
while True:
    # check for incoming subscribed topics
    mqtt.check_msg()
    
    
    
    # publish light value periodically (without using sleep)
    now = time.ticks_ms()
    if now - last_publish >= 2000:
        level = 100 - int(ldr.read()*100/4095)
        print(f'Publishing light value: {level}')
        mqtt.publish(TOPIC_LIGHT, str(level))
        last_publish = now
    
    if key != sw.value():
        if sw.value() == 1:
            mqtt.publish(TOPIC_SW, '0')
            key = sw.value()
        elif sw.value() == 0:
            mqtt.publish(TOPIC_SW, '1')
            key = sw.value()
    else:
        pass

