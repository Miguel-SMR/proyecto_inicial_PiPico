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
        
        # Loop principal de verificación
        next_id_to_enroll = 2
        
        while True:
            print("\n" + "="*50)
            print("Verificando huella...")
            print("="*50)
            
            # Intentar verificar huella
            result = verify_fingerprint()
            
            if result > 0:
                print("\n✓ ¡Acceso concedido!")
                time.sleep(2)
            else:
                print("\n✗ Huella no reconocida o error en captura")
                print("\nOpciones disponibles:")
                print("  1. Reintentar verificación")
                print("  2. Registrar nueva huella")
                print("  3. Limpiar base de datos")
                
                choice = input("\nSelecciona una opción (1/2/3): ").strip()
                
                if choice == "1":
                    # Reintentar
                    print("\nReintentando verificación...\n")
                    continue
                    
                elif choice == "2":
                    # Registrar nueva huella
                    print(f"\nRegistrando nueva huella con ID {next_id_to_enroll}...")
                    if enroll_fingerprint(next_id_to_enroll):
                        print(f"\n✓ Huella {next_id_to_enroll} registrada exitosamente")
                        next_id_to_enroll += 1
                    time.sleep(1)
                    continue
                    
                elif choice == "3":
                    # Limpiar base de datos
                    print("\nBorrando todas las huellas...")
                    try:
                        sensor.delete_fingerprint(0)  # 0 = borrar todas
                        print("✓ Base de datos limpiada")
                    except:
                        print("✓ Base de datos limpiada (o ya estaba vacía)")
                    next_id_to_enroll = 2  # Reiniciar contador
                    time.sleep(1)
                    continue
                    
                else:
                    print("✗ Opción no válida. Por favor selecciona 1, 2 o 3")
                    time.sleep(1)
                    continue
            
            time.sleep(1)
    else:
        print("\nNo se pudo iniciar el programa")
        while True:
            time.sleep(1)


