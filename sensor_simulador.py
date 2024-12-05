import random
import time
import zenoh

def simulate_sensor_data():
    # Configuración básica para Zenoh
    config = zenoh.Config()

    # Abre una sesión con Zenoh usando la configuración
    session = zenoh.open(config)

    # Crea un publicador en Zenoh para los datos de ocupación
    publisher = session.declare_publisher('office/occupancy')

    while True:
        # Genera un ID de escritorio aleatorio y un estado de ocupación aleatorio
        desk_id = random.randint(1, 10)
        occupied = random.choice([True, False])

        # Crea el payload con el estado de ocupación
        payload = f'desk/{desk_id} is {"Occupied" if occupied else "Available"}'

        # Publica el estado de ocupación en Zenoh con el publisher
        publisher.put(payload.encode('utf-8'))

        # Imprime el estado de la ocupación en la consola
        print(f'Desk {desk_id} status: {"Occupied" if occupied else "Available"}')

        # Espera 1 segundo antes de generar el siguiente dato
        time.sleep(1)

if __name__ == "__main__":
    simulate_sensor_data()








