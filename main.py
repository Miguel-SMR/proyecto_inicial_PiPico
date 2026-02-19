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

def get_device_info():
    """Obtiene información del sensor"""
    try:
        info = sensor.get_device_info()
        if info:
            print(f"\n--- Información del sensor ---")
            print(f"Modelo: {info}")
            print(f"Capacidad: {sensor.fingerprint_capacity} huellas")
            return True
        else:
            print("✓ Sensor listo (info no disponible)")
            return True
    except Exception as e:
        print(f"✓ Sensor listo (info no disponible: {e})")
        return True

def check_fingerprints_available():
    """Verifica si hay huellas registradas"""
    try:
        # Buscar el primer ID disponible
        empty_id = sensor.get_empty_id()
        if empty_id > 0:
            return True  # Hay espacio, significa que hay al menos una huella
        return False
    except:
        return False

def enroll_fingerprint(fingerprint_id=1):
    """Enrolla una nueva huella dactilar"""
    print(f"\n--- Registrando nueva huella (ID: {fingerprint_id}) ---")
    
    # Capturar huella 3 veces
    for attempt in range(3):
        print(f"\nIntento {attempt + 1}/3")
        print("Coloca tu dedo en el sensor...")
        
        # LED parpadeante azul
        sensor.ctrl_led(LEDMode.BREATHING, LEDColor.BLUE)
        
        # Capturar huella (timeout de 10 segundos)
        if sensor.collection_fingerprint(timeout=10000) == 0:
            print("✓ Huella capturada!")
            sensor.ctrl_led(LEDMode.KEEPS_ON, LEDColor.GREEN)
            
            # Esperar a que retire el dedo
            print("Retira tu dedo...")
            while sensor.detect_finger():
                time.sleep_ms(100)
            
            time.sleep(1)
        else:
            print(f"✗ Error al capturar: {sensor.get_error_description()}")
            sensor.ctrl_led(LEDMode.KEEPS_ON, LEDColor.RED)
            return False
    
    # Guardar huella
    print("\nGuardando huella...")
    if sensor.store_fingerprint(fingerprint_id) == 0:
        print(f"✓ ¡Huella registrada exitosamente! ID: {fingerprint_id}")
        sensor.ctrl_led(LEDMode.KEEPS_ON, LEDColor.GREEN)
        time.sleep(2)
        return True
    else:
        print("✗ Error al guardar la huella")
        sensor.ctrl_led(LEDMode.KEEPS_ON, LEDColor.RED)
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

# Programa principal
if __name__ == "__main__":
    print("=== Sistema de Sensor de Huella Dactilar ===\n")
    
    # Inicializar sensor
    if init_sensor():
        # Obtener información del sensor
        get_device_info()
        
        time.sleep(1)
        
        # Verificar si hay huellas registradas
        if not check_fingerprints_available():
            print("\n⚠ No hay huellas registradas en la base de datos")
            print("Es necesario registrar una huella principal primero.\n")
            
            # Enrollar primera huella
            if enroll_fingerprint(1):
                print("\n✓ Huella principal registrada correctamente")
                time.sleep(2)
                
                # Ahora verificar la huella
                print("\nVerificando la huella registrada...")
                result = verify_fingerprint()
            else:
                print("\n✗ No se puedo registrar la huella")
        else:
            print("\n✓ Hay huellas registradas. Verificando...\n")
            # Verificar una huella
            result = verify_fingerprint()
        
        # Mantener el programa corriendo
        while True:
            time.sleep(1)
    else:
        print("\nNo se pudo iniciar el programa")
        while True:
            time.sleep(1)


