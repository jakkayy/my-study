from machine import Pin, time_pulse_us, I2C, PWM
import time
import ssd1306
import network
import espnow
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS,
    TOPIC_PREFIX
)
from umqtt.simple import MQTTClient

TOPIC_DIST_CAR = f'{TOPIC_PREFIX}/dist/car'
TOPIC_RED_CAR = f'{TOPIC_PREFIX}/red/car'
TOPIC_YELLOW_CAR = f'{TOPIC_PREFIX}/yellow/car'
TOPIC_GREEN_CAR = f'{TOPIC_PREFIX}/green/car'
TOPIC_TEXT_CAR = f'{TOPIC_PREFIX}/text/car'
TOPIC_SERVO_ON = f'{TOPIC_PREFIX}/servo/on'
TOPIC_SERVO_OFF = f'{TOPIC_PREFIX}/servo/off'
TOPIC_SERVO = f'{TOPIC_PREFIX}/servo'

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
    mqtt.subscribe(TOPIC_DIST_CAR)
    mqtt.subscribe(TOPIC_RED_CAR)
    mqtt.subscribe(TOPIC_YELLOW_CAR)
    mqtt.subscribe(TOPIC_GREEN_CAR)
    mqtt.subscribe(TOPIC_TEXT_CAR)
    mqtt.subscribe(TOPIC_SERVO_ON)
    mqtt.subscribe(TOPIC_SERVO_OFF)
    mqtt.subscribe(TOPIC_SERVO)

    
def measure_distance():
    trig.off()
    time.sleep_us(2)
    trig.on()
    time.sleep_us(10)
    trig.off()

    duration = time_pulse_us(echo, 1, 30000)
    distance = (duration * 0.0343) / 2 
    return distance

def clear_oled():
    display.fill(0)
    display.show()

def clear_red():
    red.value(0)

def clear_yellow():
    yellow.value(0)

def clear_green():
    green.value(0)

    
def set_servo_angle(angle):
    minDuty = 2000 
    maxDuty = 8000
    duty = minDuty + (angle / 180) * (maxDuty - minDuty)
    servo.duty_u16(int(duty))

def setup_espnow():
    global e  # ทำให้ e ใช้งานได้ในทุกที่
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    e = espnow.ESPNow()
    e.active(True)
    


def mqtt_callback(topic, payload):
    global angle
    angle = '15'
    if topic.decode() == TOPIC_RED_CAR:
        red.value(int(payload))
    elif topic.decode() == TOPIC_YELLOW_CAR:
        yellow.value(int(payload))
    elif topic.decode() == TOPIC_GREEN_CAR:
        green.value(int(payload))
    elif topic.decode() == TOPIC_SERVO:
        print(payload.decode())
        set_servo_angle(int(payload.decode()))
        time.sleep(10)

 
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
wifi.active(True)
mqtt = MQTTClient(client_id='',
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)

e = espnow.ESPNow()
e.active(True)

mac_board1 = b'h\xb6\xb37\xf0\xfc'  #MAC ของบอร์ด 1
e.add_peer(mac_board1)


connect_wifi()
connect_mqtt()
count = 0
key = 1
angle = 0
while True:
    mqtt.check_msg()
    try:
        dist = measure_distance()
        if dist > 0:
            mqtt.publish(TOPIC_DIST_CAR, str(dist))
        # send
        e.send(mac_board1, str(dist))
        print(f"distance: {str(dist)}")
        
        #recieve
        host, msg = e.recv()
        if msg:
            if msg.decode() == '1':
                key = 1
            if msg.decode() == '0':
                key = 0
            if msg.decode() not in ['1','0']:
                distance_received = msg.decode()
                print(f"Received from board1: {distance_received}")
                d1 = float(distance_received) 
                print(f"Distance received: {d1}")
            
            if d1 <= 10 and dist > 10 and count == 0 and key == 0:
                clear_green()
                clear_oled()
                count += 1
                red.value(1)
                display.text("stop", 50, 25)
                set_servo_angle(110)
            elif d1 <= 10 and dist > 10 and count == 0 and key == 1:
#                 clear_green()
#                 clear_oled()
#                 count += 1
#                 red.value(1)
#                 display.text("stop", 50, 25)
#                 set_servo_angle(110)
                clear_red()
                clear_oled()
                count = 0
                green.value(1)
                display.text("go", 50, 25)
                set_servo_angle(15)
            elif d1 <= 10 and dist > 10 and count == 0 and key == 0:
                clear_red()
#                 clear_oled()
                green.value(1)
                display.text("go", 50, 25)
                set_servo_angle(15)
#                 count += 1
#                 red.value(1)
#                 display.text("stop", 50, 25)
#                 set_servo_angle(110)
            elif d1 <= 10 and dist > 10 and count != 0 and key == 1:
                clear_red()
#                 clear_oled()
                count = 0
                green.value(1)
                display.text("go", 50, 25)
                set_servo_angle(15)
            elif d1 <= 10 and dist > 10 and count != 0 and key == 0:
                clear_green()
#                 clear_oled()
                count += 1
                red.value(1)
                display.text("stop", 50, 25)
                set_servo_angle(110)
            elif d1 <= 10 and dist > 10 and count == 0 and key == 1:
                clear_red()
#                 clear_oled()
                count = 0
                green.value(1)
                display.text("go", 50, 25)
                set_servo_angle(15)
            elif d1 <= 10 and dist <= 10 and count != 0 and key == 0:
                clear_green()
#                 clear_oled()
                count += 1
                red.value(1)
                display.text("stop", 50, 25)
                set_servo_angle(110)
            elif d1 <= 10 and dist <= 10 and count != 0 and key == 1:
                clear_red()
#                 clear_oled()
                count = 0
                green.value(1)
                display.text("go", 50, 25)
                set_servo_angle(15)
            elif d1 <= 10 and dist <= 10 and count == 0 and key == 1:
                clear_red()
#                 clear_oled()
                count = 0
                green.value(1)
                display.text("go", 50, 25)
                set_servo_angle(15)
            elif d1 <= 10 and dist <= 10 and count == 0 and key == 0:
                clear_red()
#                 clear_oled()
                count = 0
                green.value(1)
                display.text("go", 50, 25)
                set_servo_angle(15)
            elif d1 > 10 and dist > 10 and count == 0 and key == 0:
                clear_red()
                clear_oled()
                count = 0
                green.value(1)
                display.text("go", 50, 25)
                set_servo_angle(15)
            elif d1 > 10:
                clear_red()
                clear_oled()
                count = 0
                green.value(1)
                display.text("go", 50, 25)
                set_servo_angle(15)
        print('count: ',count)
        print('key: ',key)
        display.show()
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        print("ESP-NOW not found. Restarting...")
        setup_espnow()
        time.sleep(1)
