from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time

# Configuración del LED
led = Pin('LED', Pin.OUT)

# Configuración de la pantalla OLED
WIDTH = 128
HEIGHT = 64
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Tamaño de la pelota (cuadrado)
BALL_SIZE = 4

# Posición y velocidad inicial
x = 10
y = 10
dx = 2
dy = 1

while True:
    oled.fill(0)  # Limpiar pantalla

    # Dibujar la pelota (cuadrado relleno)
    oled.fill_rect(x, y, BALL_SIZE, BALL_SIZE, 1)

    # Actualizar posición
    x += dx
    y += dy

    # Detectar colisiones con los bordes
    collision = False
    if x <= 0 or x + BALL_SIZE >= WIDTH:
        dx = -dx
        collision = True
    if y <= 0 or y + BALL_SIZE >= HEIGHT:
        dy = -dy
        collision = True

    # Si hubo colisión, hacer parpadear el LED
    if collision:
        led.toggle()

    oled.show()      # Mostrar los cambios en la pantalla
    time.sleep(0.05) # Pequeña pausa para controlar la velocidad