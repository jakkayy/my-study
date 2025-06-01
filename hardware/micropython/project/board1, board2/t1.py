from machine import Pin, ADC, I2C, time_pulse_us
import utime
import ssd1306
import time
import network
import espnow
from config import (
    WIFI_SSID, WIFI_PASS,
    MQTT_BROKER, MQTT_USER, MQTT_PASS,
    TOPIC_PREFIX
)
from umqtt.simple import MQTTClient

TOPIC_DIST_HUMAN = f'{TOPIC_PREFIX}/dist/human'
TOPIC_RED_HUMAN = f'{TOPIC_PREFIX}/red/human'
TOPIC_YELLOW_HUMAN = f'{TOPIC_PREFIX}/yellow/human'
TOPIC_GREEN_HUMAN = f'{TOPIC_PREFIX}/green/human'
TOPIC_TEXT_HUMAN = f'{TOPIC_PREFIX}/text/human'
TOPIC_CROSS_COUNT = f'{TOPIC_PREFIX}/cross_count'
TOPIC_LAST_CROSS = f'{TOPIC_PREFIX}/last_cross'
TOPIC_AVG_CROSS = f'{TOPIC_PREFIX}/avg_cross'
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
    mqtt.subscribe(TOPIC_DIST_HUMAN)
    mqtt.subscribe(TOPIC_RED_HUMAN)
    mqtt.subscribe(TOPIC_YELLOW_HUMAN)
    mqtt.subscribe(TOPIC_GREEN_HUMAN)
    mqtt.subscribe(TOPIC_TEXT_HUMAN)
    mqtt.subscribe(TOPIC_CROSS_COUNT)
    mqtt.subscribe(TOPIC_LAST_CROSS)
    mqtt.subscribe(TOPIC_SERVO)

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

def setup_espnow():
    global e  # ทำให้ e ใช้งานได้ในทุกที่
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    e = espnow.ESPNow()
    e.active(True)

# สถิติการข้าม
cross_count = 0  # จำนวนครั้งที่มีคนข้าม
last_cross_time = None  # เวลาที่ข้ามครั้งล่าสุด
total_cross_time = 0  # เวลาทั้งหมดที่มีคนข้าม
avg_cross_time = 0  # เวลาข้ามเฉลี่ย

def send_cross_stats():
    global cross_count, last_cross_time, total_cross_time, avg_cross_time
    
    current_time = utime.ticks_ms()  # ใช้เวลาจากระบบ
    if last_cross_time is not None:
        time_diff = utime.ticks_diff(current_time, last_cross_time)  # ห่างเวลาระหว่างการข้ามล่าสุด
        total_cross_time += time_diff
        avg_cross_time = total_cross_time // cross_count  # คำนวณเวลาเฉลี่ย
    
    last_cross_time = current_time  # อัปเดตเวลาที่ข้ามล่าสุด
    cross_count += 1  # เพิ่มจำนวนการข้าม
    text = ''
    t = avg_cross_time // 1000
    if avg_cross_time // 1000 < 60:
        text = f"{t} วินาที"
    else:
        t1 = t//60
        t2 = t -t1
        text = f"{t1} นาที {t2} วินาที"
    
    mqtt.publish(TOPIC_LAST_CROSS, str(time.localtime(last_cross_time)))
    print("ส่งสถิติการข้าม:")

def mqtt_callback(topic, payload):
#     if topic.decode() == TOPIC_SERVO:
#         red.value(0)
#         print(payload.decode())
#         green.value(1)
#         time.sleep(10)
    if topic.decode() == TOPIC_RED_HUMAN:
        green.value(0)
        red.value(int(payload))
        time.sleep(8)
    elif topic.decode() == TOPIC_GREEN_HUMAN:
        red.value(0)
        green.value(int(payload))
        time.sleep(8)
    
def send_cross_stats():
    global cross_count, last_cross_time, total_cross_time, avg_cross_time
    
    current_time = utime.ticks_ms()  # ใช้เวลาจากระบบ
    if last_cross_time is not None:
        time_diff = utime.ticks_diff(current_time, last_cross_time)  # ห่างเวลาระหว่างการข้ามล่าสุด
        total_cross_time += time_diff
        avg_cross_time = total_cross_time // cross_count  # คำนวณเวลาเฉลี่ย
    
    last_cross_time = current_time  # อัปเดตเวลาที่ข้ามล่าสุด
    cross_count += 1  # เพิ่มจำนวนการข้าม
    
    stats_msg = {
        "cross_count": cross_count,
        "last_cross_time": time.localtime(last_cross_time),
        "avg_cross_time": avg_cross_time // 1000  # แปลงเวลามิลลิวินาทีเป็นวินาที
    }
    
    mqtt.publish(TOPIC_CROSS_COUNT, str(cross_count))  # ส่งข้อมูลสถิติไปยัง Node-RED
    print("ส่งสถิติการข้าม:", stats_msg)

def send_cross_time():
    t = time.localtime(time.time())  # แปลงเป็นเวลาไทย (GMT+7)
    hour, minute = t[3], t[4]  # ดึงเฉพาะ ชั่วโมง:นาที
    time_str = "{:02d}:{:02d}".format(hour, minute)

    print("🚶‍♂️ คนข้ามล่าสุด: ", time_str)
    mqtt.publish(TOPIC_LAST_CROSS, time_str.encode())




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
wifi.active(True)
mqtt = MQTTClient(client_id='',
                  server=MQTT_BROKER,
                  user=MQTT_USER,
                  password=MQTT_PASS)

e = espnow.ESPNow()
e.active(True)

mac_board2 = b'h\xb6\xb38\x02L'  #MAC ของบอร์ด 2
e.add_peer(mac_board2)



connect_wifi()
connect_mqtt()
last_publish = 0
mqtt.publish(TOPIC_CROSS_COUNT, '0')
key = 1
count = 0
r = 0
traf = 0
switch = 1
s = 0
while True:
    mqtt.check_msg()    
    try:
        dist = measure_distance()
        # send
#         now = time.ticks_ms()
#         if now - last_publish >= 1000:
#             e.send(mac_board2, str(dist))
#             print(f"distance: {str(dist)}")
#             mqtt.publish(TOPIC_DIST_HUMAN, str(dist))
#             last_publish = now
        e.send(mac_board2, str(dist))
        print(f"distance: {str(dist)}")
        mqtt.publish(TOPIC_DIST_HUMAN, str(dist))
#         
        # recieve
        host, msg = e.recv()
        if msg:
            distance_received = msg.decode()
            print(f"Received from board2: {distance_received}")
            d2 = float(distance_received)  # แปลงเป็น float
            print(f"Distance received: {d2}")
            clear()
            if dist <= 10:
                clear()
                red.value(1)
                display.text("you want cross?",0 ,10)
                display.text("Press the button",0 ,25)               
                r = 0
                if sw.value() == 0:
                    send_cross_time()
                    send_cross_stats()
                    switch = 0
                    traf += 1
                    if d2 > 10:
                        clear()
                        key = 0
                        e.send(mac_board2, str(key))
                        count += 1
                        display.text("GO", 50, 25)
                        mqtt.publish(TOPIC_TEXT_HUMAN, 'GO')
                        green.value(1)
                        buzzer.value(1)
                        time.sleep_ms(500) 
                        buzzer.value(0)
                        traf = 0
                        time.sleep(0.1)
                    elif d2 <= 10 and count == 1 and key == 0 and traf == 0:
                        key = 1
                        if s == 0:
                            e.send(mac_board2, '5')
                            e.send(mac_board2, str(key))
                            time.sleep(1)
                        clear()
                        red.value(0)
                        count = 0
                        traf += 1
                        red.value(1)
                        display.text("wait", 50, 25)
                        s += 1
                    elif d2 <= 10 and count != 0:
                        key = 0
                        count += 1
                        green.value(1)
                        display.text("GO", 50, 25)
                        mqtt.publish(TOPIC_TEXT_HUMAN, 'GO')
                        traf = 0
                        s = 0
                    elif d2 <= 10 and count == 0 and key == 1 and traf == 1:
                        key = 1
                        if s == 0:
                            e.send(mac_board2, '5')
                            e.send(mac_board2, str(key))
                            time.sleep(1)
                        clear()
                        count = 0
                        traf += 1
                        red.value(1)
                        display.text("wait", 50, 25)
                        s += 1
                    elif d2 > 10 and count == 0 and key == 1 and traf == 0:
                        key = 0
                        count += 1
                        green.value(1)
                        display.text("GO", 50, 25)
                        mqtt.publish(TOPIC_TEXT_HUMAN, 'GO')
                        traf = 0
                        s = 0
                    elif d2 <= 10 and count == 0 and key == 1 and traf == 0:
                        key = 1
                        if s == 0:
                            e.send(mac_board2, '5')
                            e.send(mac_board2, str(key))
                            time.sleep(1)
                        clear()
                        
                        count = 0
                        red.value(1)
                        display.text("wait", 50, 25)
                        mqtt.publish(TOPIC_TEXT_HUMAN, 'wait')
                        traf = 1
                        s += 1
                    elif d2 <= 10 and count == 0 and key == 1 and traf != 0:
                        clear()
                        key = 1
                        e.send(mac_board2, str(key))
                        count = 0
                        red.value(1)
                        display.text("wait", 50, 25)
                        mqtt.publish(TOPIC_TEXT_HUMAN, 'wait')
#                         e.send(mac_board2, '5')
#                         time.sleep(0.1)
                    elif d2 > 10 and count == 0 and key == 1 and traf != 0:
                        if s == 0:
                            e.send(mac_board2, '5')
                            e.send(mac_board2, str(key))
                            time.sleep(1)
                        clear()
                        key = 1
                        count = 0
                        red.value(1)
                        display.text("wait", 50, 25)
                        mqtt.publish(TOPIC_TEXT_HUMAN, 'wait')
                        s += 1
                    else:
                        pass
                elif d2 > 10 and dist <= 10 and count == 1 and key == 0 and traf == 0:
                    clear()
                    green.value(1)
                    display.text("GO", 50, 25)
                    mqtt.publish(TOPIC_TEXT_HUMAN, 'GO')
                    traf = 0
                    s = 0
                elif d2 > 10 and dist <= 10 and count == 1 and key == 0 and traf == 3:
                    clear()
                    green.value(1)
                    display.text("GO", 50, 25)
                    mqtt.publish(TOPIC_TEXT_HUMAN, 'GO')
                    traf = 0
                    s = 0
                elif key == 0:
                    clear()
                    green.value(1)
                    display.text("GO", 50, 25)
                    mqtt.publish(TOPIC_TEXT_HUMAN, 'GO')
                    traf = 0
                    s = 0
                    e.send(mac_board2, '5')
                    time.sleep(0.1)
                elif d2 <= 10 and key == 1 and traf == 2:
                    if s == 0:
                            e.send(mac_board2, '5')
                            e.send(mac_board2, str(key))
                            time.sleep(1)
                    clear()
                    count = 0
                    red.value(1)
                    display.text("wait", 50, 25)
                    mqtt.publish(TOPIC_TEXT_HUMAN, 'wait')
                    s += 1
                elif d2 > 10 and count == 0 and key == 1 and traf == 0 and switch == 0:
                    clear()
                    if s == 0:
                        e.send(mac_board2, '5')
                        time.sleep(1)
                    green.value(1)
                    display.text("GO", 50, 25)
                    mqtt.publish(TOPIC_TEXT_HUMAN, 'GO')
                    traf = 0
                    s += 1
                elif d2 > 10 and key == 1 and traf == 2:
                    clear()
                    green.value(1)
                    display.text("GO", 50, 25)
                    mqtt.publish(TOPIC_TEXT_HUMAN, 'GO')
                    traf = 0
                    s = 0
                elif key == 1 and traf != 0:
                    clear()
                    count = 0
                    red.value(1)
                    display.text("STOP", 50, 25)
                    mqtt.publish(TOPIC_TEXT_HUMAN, 'STOP')
#                     e.send(mac_board2, '12')
                    switch = 1
#                 else:
#                     clear()
#                     count = 0
#                     red.value(1)
#                     display.text("STOP", 50, 25)
            else:
                clear()
                if r == 0:
                    e.send(mac_board2, str(key))
                    e.send(mac_board2, '12')
                    time.sleep(1)
                r+= 1
                key = 1
                count = 0
                red.value(1)
                display.text("STOP", 50, 25)
                mqtt.publish(TOPIC_TEXT_HUMAN, 'STOP')             
                switch = 1
        print('count: ',count)
        print('key: ',key)
        print('traf: ',traf) 
        display.show()
        time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
        print("ESP-NOW not found. Restarting...")
        setup_espnow()
        time.sleep(1)
