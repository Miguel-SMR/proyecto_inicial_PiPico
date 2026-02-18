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

# Velocidad máxima permitida (para que no sea demasiado rápida)
MAX_SPEED = 10

while True:
    oled.fill(0)  # Limpiar pantalla

    # Dibujar la pelota (cuadrado relleno)
    oled.fill_rect(x, y, BALL_SIZE, BALL_SIZE, 1)

    # Mostrar coordenadas y velocidad en texto
    oled.text(f"X:{x:3d} Y:{y:3d}", 0, 0, 1)
    oled.text(f"DX:{dx:2d} DY:{dy:2d}", 0, 8, 1)

    # Actualizar posición
    x += dx
    y += dy

    # Detectar colisiones con los bordes
    collision_x = False
    collision_y = False

    if x <= 0 or x + BALL_SIZE >= WIDTH:
        dx = -dx
        collision_x = True
    if y <= 0 or y + BALL_SIZE >= HEIGHT:
        dy = -dy
        collision_y = True

    # Si hubo colisión en algún eje, aumentar la velocidad correspondiente
    if collision_x:
        # Aumentar velocidad horizontal, manteniendo la dirección
        dx = (abs(dx) + 1) * (1 if dx > 0 else -1)
        # Limitar a velocidad máxima
        if abs(dx) > MAX_SPEED:
            dx = MAX_SPEED * (1 if dx > 0 else -1)
        led.toggle()  # Parpadeo del LED en cada rebote

    if collision_y:
        dy = (abs(dy) + 1) * (1 if dy > 0 else -1)
        if abs(dy) > MAX_SPEED:
            dy = MAX_SPEED * (1 if dy > 0 else -1)
        led.toggle()  # Parpadeo adicional si es doble rebote

    oled.show()
    time.sleep(0.05)
