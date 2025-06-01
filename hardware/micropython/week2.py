from machine import Pin, ADC
import time

ldr = ADC(Pin(4))
ldr.atten(ADC.ATTN_11DB)

while True:
    print(ldr.read())
    time.sleep(0.1)