from machine import Pin, ADC
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
TOPIC_LED_RED = f'{TOPIC_PREFIX}/led/red'


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
    mqtt.subscribe(TOPIC_LED_RED)
    print('MQTT broker connected.')


def mqtt_callback(topic, payload):
    if topic.decode() == TOPIC_LED_RED:
        try:
            red.value(int(payload))
        except ValueError:
            pass


############
# setup
############
red = Pin(RED_GPIO, Pin.OUT)
ldr = ADC(Pin(LDR_GPIO), atten=ADC.ATTN_11DB)
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

