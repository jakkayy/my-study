from machine import Pin, time_pulse_us
import time

TRIG_PIN = 5
ECHO_PIN = 6

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

def measure_distance():
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    duration = time_pulse_us(echo, 1, 30000)
    distance = (duration * 0.0343) / 2
    return distance

while True:
    dist = measure_distance()
    print(f"Distance: {dist:.2f} cm")
    time.sleep(0.5)