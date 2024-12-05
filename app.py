import zenoh
from flask import Flask, render_template, jsonify
import threading
import time

app = Flask(__name__)

# Lista para almacenar los datos de ocupación (inicializamos todos los escritorios como disponibles)
occupancy_data = [{"id": str(i), "status": "Available"} for i in range(1, 11)]  # desk 1 a desk 10

# Lock para manejar la concurrencia
data_lock = threading.Lock()

# Función para procesar los datos de ocupación recibidos
def process_occupancy_data(change):
    global occupancy_data
    payload = change.payload.to_bytes().decode('utf-8')
    desk_id_raw, status = payload.split(' is ')
    desk_id = desk_id_raw.split('/')[1]  # Extraer solo el número después de 'desk/'

    print(f"Received data: {payload}")  # Imprimir los datos recibidos

    # Actualizar el estado del escritorio en la lista
    with data_lock:
        for desk in occupancy_data:
            if desk["id"] == desk_id:
                if desk["status"] != status:  # Solo actualizar si hay un cambio
                    print(f"Updating desk {desk_id} status from {desk['status']} to {status}")
                    desk["status"] = status
                break

    print("Current occupancy data:", occupancy_data)  # Verifica los cambios

# Función para iniciar el servidor Zenoh en un hilo
def start_zenoh_server():
    config = zenoh.Config()
    session = zenoh.open(config)
    session.declare_subscriber('office/occupancy', process_occupancy_data)

    print("Servidor Zenoh activo. Esperando datos...")
    while True:
        time.sleep(1)

# Ruta para obtener los datos de ocupación
@app.route('/occupancy')
def get_occupancy():
    with data_lock:
        return jsonify(occupancy_data)

# Ruta principal para la visualización
@app.route('/')
def index():
    return render_template('index.html', occupancy=occupancy_data)

if __name__ == "__main__":
    # Inicia el servidor Zenoh en un hilo separado
    threading.Thread(target=start_zenoh_server, daemon=True).start()
    app.run(debug=True)

