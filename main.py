from machine import Pin, I2C
import time

# Configuración del LED
led = Pin('LED', Pin.OUT)


i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)

