from machine import Pin, I2C
import time
from dfrobot_id809 import DFRobot_ID809_I2C, LEDMode, LEDColor

# Configuración del LED
led = Pin('LED', Pin.OUT)

# Configuración del I2C para el sensor
i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)

# Inicializar el sensor
sensor = DFRobot_ID809_I2C(i2c)

def init_sensor():
    """Inicializa el sensor de huella dactilar"""
    print("Inicializando sensor...")
    
    if sensor.begin():
        print("✓ Sensor inicializado correctamente!")
        
        # Verificar conexión
        if sensor.is_connected():
            print("✓ Sensor conectado!")
            return True
        else:
            print("✗ Error: Sensor no conectado")
            return False
    else:
        print("✗ Error: No se pudo inicializar el sensor")
        led.on()  # Enciende el LED del Pico como indicador de error
        return False

def get_led_modes():
    """Obtiene todos los modos de LED disponibles"""
    modes = []
    for attr in dir(LEDMode):
        if not attr.startswith('_'):
            modes.append((attr, getattr(LEDMode, attr)))
    return modes

def get_led_colors():
    """Obtiene todos los colores de LED disponibles"""
    colors = []
    for attr in dir(LEDColor):
        if not attr.startswith('_'):
            colors.append((attr, getattr(LEDColor, attr)))
    return colors

def demo_all_led_functions():
    """Demostración de todas las funciones de LED rotando entre modos y colores"""
    print("\n=== DEMOSTRACIÓN DE FUNCIONES DE LED ===\n")
    
    # Obtener todos los modos y colores
    modes = get_led_modes()
    colors = get_led_colors()
    
    print(f"Modos de LED encontrados: {len(modes)}")
    for mode_name, _ in modes:
        print(f"  - {mode_name}")
    
    print(f"\nColores de LED encontrados: {len(colors)}")
    for color_name, _ in colors:
        print(f"  - {color_name}")
    
    print("\n--- Rotando entre todas las combinaciones ---\n")
    
    counter = 0
    
    # Mientras True - rotando infinitamente
    while True:
        for mode_name, mode_value in modes:
            for color_name, color_value in colors:
                counter += 1
                
                # Aplicar la combinación
                sensor.ctrl_led(mode_value, color_value)
                
                # Mostrar información
                print(f"[{counter}] Modo: {mode_name:<15} | Color: {color_name:<10}", end="")
                
                # Esperar 2 segundos para ver el efecto
                time.sleep(2)
                
                # Limpiar la línea y mostrar lo siguiente
                print("\r", end="")
        
        print("\n--- Ciclo completado, reiniciando ---\n")
        time.sleep(1)

# Programa principal
if __name__ == "__main__":
    print("=== Demostración de LED del Sensor ID809 ===\n")
    
    # Inicializar sensor
    if init_sensor():
        print("\n✓ Sensor listo para la demostración\n")
        
        # Ejecutar demostración de LEDs
        demo_all_led_functions()
    else:
        print("\nNo se pudo iniciar el programa")
        while True:
            time.sleep(1)


