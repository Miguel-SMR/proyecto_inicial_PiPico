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
            
            # Encender LED verde
            sensor.ctrl_led(LEDMode.KEEPS_ON, LEDColor.GREEN)
            print("✓ LED activado!")
            
            return True
        else:
            print("✗ Error: Sensor no conectado")
            sensor.ctrl_led(LEDMode.KEEPS_ON, LEDColor.RED)
            return False
    else:
        print("✗ Error: No se pudo inicializar el sensor")
        led.on()  # Enciende el LED del Pico como indicador de error
        return False

def verify_fingerprint():
    """Verifica una huella dactilar"""
    print("\n--- Verificando huella ---")
    print("Coloca tu dedo en el sensor...")
    
    # LED parpadeante azul mientras espera
    sensor.ctrl_led(LEDMode.BREATHING, LEDColor.BLUE)
    
    # Capturar huella (timeout de 10 segundos)
    if sensor.collection_fingerprint(timeout=10000) == 0:
        print("Huella capturada, buscando en la base de datos...")
        
        # Buscar huella en la base de datos
        result = sensor.search()
        
        if result > 0:
            print(f"✓ ¡Huella reconocida! ID: {result}")
            sensor.ctrl_led(LEDMode.KEEPS_ON, LEDColor.GREEN)
            return result
        else:
            print("✗ Huella no reconocida")
            sensor.ctrl_led(LEDMode.KEEPS_ON, LEDColor.RED)
            return -1
    else:
        print(f"✗ Error al capturar huella: {sensor.get_error_description()}")
        sensor.ctrl_led(LEDMode.KEEPS_ON, LEDColor.RED)
        return -1

def get_device_info():
    """Obtiene información del sensor"""
    info = sensor.get_device_info()
    if info:
        print(f"\n--- Información del sensor ---")
        print(f"Modelo: {info}")
        print(f"Capacidad: {sensor.fingerprint_capacity} huellas")
    else:
        print("✗ No se pudo obtener información del sensor")

# Programa principal
if __name__ == "__main__":
    print("=== Sistema de Sensor de Huella Dactilar ===\n")
    
    # Inicializar sensor
    if init_sensor():
        # Obtener información del sensor
        get_device_info()
        
        # Esperar un poco
        time.sleep(1)
        
        # Ejemplo: Verificar una huella
        result = verify_fingerprint()
        
        # Mantener el programa corriendo
        while True:
            time.sleep(1)
    else:
        print("\nNo se pudo iniciar el programa")
        while True:
            time.sleep(1)


