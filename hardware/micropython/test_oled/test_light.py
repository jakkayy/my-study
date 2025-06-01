from machine import Pin,I2C
i2c = I2C(0, sda=Pin(48), scl=Pin(47))
display.text("Hello world",0 0)
display.show()