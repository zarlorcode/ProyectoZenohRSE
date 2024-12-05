import zenoh

def process_occupancy_data(change):
    # Convierte el payload de ZBytes a bytes y luego decodifica
    payload = change.payload.to_bytes().decode('utf-8')
    # Imprime el estado del escritorio
    print(f"Received data: {payload}")

def start_server():
    # Configuración básica para Zenoh
    config = zenoh.Config()

    # Abre una sesión con Zenoh usando la configuración
    session = zenoh.open(config)

    # Declara un suscriptor para los datos de ocupación
    subscriber = session.declare_subscriber('office/occupancy', process_occupancy_data)

    # Mensaje de confirmación
    print("Servidor suscrito a los datos de ocupación. Esperando actualizaciones...")

    # Espera indefinida para recibir datos
    input("Presiona Enter para salir...\n")

if __name__ == "__main__":
    start_server()



