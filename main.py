from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
 
# --- CONFIGURACIÓN DE PANTALLA ---
WIDTH = 128
HEIGHT = 64
# Asegúrate de que los pines coincidan con tu placa (ej. Raspberry Pi Pico: scl=17, sda=16)
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
