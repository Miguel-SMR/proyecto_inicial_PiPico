from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
 
pin = Pin('LED', Pin.OUT)  # Pin integrado del LED en Raspberry Pi Pico

# --- CONFIGURACIÓN DE PANTALLA ---
WIDTH = 128
HEIGHT = 64
# Asegúrate de que los pines coincidan con tu placa (ej. Raspberry Pi Pico: scl=17, sda=16)
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

def parpadear_led(veces, intervalo):
    for _ in range(veces):
        pin.value(1)  # Encender LED
        time.sleep(intervalo)
        pin.value(0)  # Apagar LED
        time.sleep(intervalo)

def ensenar_contenido(sleep_time):
    oled.show()  # Mostrar cambios
    time.sleep(sleep_time)

def interaccion_pantalla():
    oled.fill(1)  # Llenar pantalla de blanco
    ensenar_contenido(1)
    oled.fill(0)  # Limpiar pantalla
    ensenar_contenido(1)
    oled.text("Hola, Mundo!", 0, 0)  # Escribir texto en la pantalla
    ensenar_contenido(1)
    oled.text("Raspberry Pico", 0, 10)  # Escribir más texto
    ensenar_contenido(1)
    oled.fill(0)  # Limpiar pantalla
    ensenar_contenido(1)
    oled.rect(10, 10, 50, 30, 1)  # Dibujar un rectángulo
    ensenar_contenido(1)
    oled.pixel(20, 20, 1)  # Dibujar un pixel
    ensenar_contenido(1)
    oled.fill(0)  # Limpiar pantalla
    oled.show()  # Mostrar cambios

while True:
    parpadear_led(7, 0.2)  # Parpadear el LED 5 veces con un intervalo de 0.5 segundos
    interaccion_pantalla()  # Interactuar con la pantalla OLED
    time.sleep(2)  # Esperar antes de repetir el ciclo