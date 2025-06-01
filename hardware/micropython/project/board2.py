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
TOPIC_TEXT_CAR = f'{TOPIC_PREFIX}/text/car'
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
    mqtt.subscribe(TOPIC_TEXT_CAR)
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

def clear_red():
    red.value(0)

def clear_yellow():
    yellow.value(0)

def clear_green():
    green.value(0)

def stop():
    clear_oled()
    clear_green()
    display.text("stop", 50, 25)
    red.value(1)
    set_servo_angle(110)
    print('s')

def go():
    clear_oled()
    clear_red()
    display.text("go", 50, 25)
    green.value(1)
    set_servo_angle(15)
    print('g')
    
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
    if topic.decode() == TOPIC_SERVO:
        print(payload.decode())
        green.value(0)
        red.value(1)
        display.text("stop", 50, 25)
        set_servo_angle(int(payload.decode()))
        display.show()
        time.sleep(10)
        clear_oled()
        clear_red()
#     elif topic.decode() == TOPIC_RED_CAR:
#         green.value(0)
#         red.value(int(payload))
#         time.sleep(8)
#     elif topic.decode() == TOPIC_GREEN_CAR:
#         red.value(0)
#         green.value(int(payload))
#         time.sleep(8)

 
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

key = 1
count = 0
connect_wifi()
connect_mqtt()
while True:
    mqtt.check_msg()
    try:
        
        dist = measure_distance()
        # send

        e.send(mac_board1, str(dist))
        print(f"distance: {str(dist)}")
        mqtt.publish(TOPIC_DIST_CAR, str(dist))
#         
        #recieve
        host, msg = e.recv()
        if msg is not None:
            distance_received = msg.decode()
            if msg.decode() in ['1','0']:
                key = msg.decode()
            elif msg.decode() not in ['1','0']:
                d1 = float(distance_received) 
            print(f"Distance received: {d1}")
            if dist > 10:
                if key == '0':
                    if d1 <= 10:
                        clear_oled()
                        clear_green()
                        display.text("stop", 50, 25)
                        mqtt.publish(TOPIC_TEXT_CAR, 'stop')
                        red.value(1)
                        set_servo_angle(110)
                        count = 0
                        print('s')
                    elif d1 > 10:
                        mqtt.check_msg()
                        clear_oled()
                        clear_red()
                        display.text("go", 50, 25)
                        mqtt.publish(TOPIC_TEXT_CAR, 'go')
                        green.value(1)
                        set_servo_angle(15)
                        count += 1
                        print('g')
                elif key == '1':
                    if d1 <= 10:
                        mqtt.check_msg()
                        clear_oled()
                        clear_red()
                        display.text("go", 50, 25)
                        mqtt.publish(TOPIC_TEXT_CAR, 'go')
                        green.value(1)
                        set_servo_angle(15)
                        count += 1
                        print('t')
                    elif d1 > 10:
                        mqtt.check_msg()
                        clear_oled()
                        clear_red()
                        display.text("go", 50, 25)
                        mqtt.publish(TOPIC_TEXT_CAR, 'go')
                        green.value(1)
                        set_servo_angle(15)
                        count += 1
                        print('t')
            elif dist <= 10:
                if key == '0':
                    if d1 > 10:
                        mqtt.check_msg()
                        clear_oled()
                        clear_red()
                        display.text("go", 50, 25)
                        mqtt.publish(TOPIC_TEXT_CAR, 'go')
                        green.value(1)
                        set_servo_angle(15)
                        count += 1
                    elif d1 >= 10:
                        clear_oled()
                        clear_green()
                        display.text("stop", 50, 25)
                        mqtt.publish(TOPIC_TEXT_CAR, 'stop')
                        red.value(1)
                        set_servo_angle(110)
                        count = 0
                        print('s')
                elif key == '1':
                    mqtt.check_msg()
                    clear_oled()
                    clear_red()
                    display.text("go", 50, 25)
                    mqtt.publish(TOPIC_TEXT_CAR, 'go')
                    green.value(1)
                    set_servo_angle(15)

                    print(8)
        print(key)
        display.show()
        time.sleep_ms(100)
    except Exception as e:
        print(f"Error: {e}")
        print("ESP-NOW not found. Restarting...")
        setup_espnow()
        time.sleep(1)

