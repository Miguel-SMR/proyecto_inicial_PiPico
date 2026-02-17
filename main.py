from machine import Pin, I2C, RTC
from ssd1306 import SSD1306_I2C
import time
 
pin = Pin('LED', Pin.OUT)  # Pin integrado del LED en Raspberry Pi Pico
rtc = RTC()  # Inicializar el reloj real time (RTC)
# --- CONFIGURACIÓN DE PANTALLA ---
WIDTH = 128
HEIGHT = 64

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

rtc.datetime((2026, 2, 17, 2, 15, 21, 0, 0))  # Establecer fecha y hora (año, mes, día, día de la semana, hora, minuto, segundo, milisegundo)

while True:
    fecha = rtc.datetime()  # Obtener la fecha y hora actual
    hora = f"{fecha[4]:02d}:{fecha[5]:02d}:{fecha[6]:02d}"  # Formatear la hora
    
    oled.fill(0)  # Limpiar la pantalla
    oled.text("Reloj Pico", 30, 10, 1)

    oled.text(hora, 30, 30, 1)  # Mostrar la hora en la pantalla
    oled.text(f"{fecha[2]:02d}/{fecha[1]:02d}/{fecha[0]}", 30, 50, 1)  # Mostrar la fecha en formato DD/MM/YYYY
    oled.show()  # Actualizar la pantalla
    pin.toggle()  # Alternar el estado del LED integrado
    time.sleep(1)  # Esperar 1 segundo antes de actualizar la hora nuevamente

