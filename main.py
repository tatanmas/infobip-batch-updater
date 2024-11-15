import pandas as pd
import json
import requests
from tqdm import tqdm
from dotenv import load_dotenv
import os
import logging
import time
import chardet  # Detectar codificación del archivo

# Configuración de logging para usuarios no técnicos
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener variables de entorno
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
CSV_FILE = os.getenv("CSV_FILE")

# Validar que todas las variables de entorno estén presentes
if not all([API_KEY, BASE_URL, CSV_FILE]):
    logging.error("⚠️ Faltan variables de entorno. Por favor, verifica el archivo .env.")
    exit(1)

# Endpoint para la actualización en lote de perfiles
INFOBIP_BATCH_ENDPOINT = f"{BASE_URL}/people/2/persons"

# Detectar y leer el archivo CSV con la codificación adecuada
def read_csv(file_path):
    if not os.path.exists(file_path):
        logging.error(f"⚠️ El archivo '{file_path}' no existe.")
        exit(1)
    try:
        # Detectar la codificación del archivo
        with open(file_path, "rb") as file:
            result = chardet.detect(file.read())
        encoding = result["encoding"]
        logging.info(f"📂 Detectada codificación del archivo: {encoding}")

        # Leer el archivo CSV con la codificación detectada
        data = pd.read_csv(file_path, encoding=encoding)
        logging.info(f"📂 Archivo CSV '{file_path}' leído correctamente.")
        return data
    except Exception as e:
        logging.error(f"⚠️ Error al leer el archivo CSV: {e}")
        exit(1)

# Crear el payload para la API
def create_payload(data):
    payload = []
    for _, row in data.iterrows():
        person = {
            "firstName": row.get("Nombre", ""),
            "customAttributes": {
                "onboarding_hr": str(row.get("onboarding_hr", "False")).lower() == "true"
            },
            "contactInformation": {
                "phone": [{"number": str(row.get("phone", ""))}]
            }
        }
        payload.append(person)
    logging.info(f"✅ Payload creado con {len(payload)} registros.")
    return payload

# Enviar un lote a la API de Infobip
def send_batch(api_key, payload):
    headers = {
        "Authorization": f"App {api_key}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(INFOBIP_BATCH_ENDPOINT, headers=headers, json={"people": payload})
        # Mostrar respuesta de la API en la terminal
        logging.info(f"📡 Respuesta de la API: {response.status_code} - {response.text}")
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"⚠️ Error en la solicitud a la API: {e}")
        return None

# Procesar y enviar los datos en lotes
def process_and_send():
    # Leer datos del archivo CSV
    data = read_csv(CSV_FILE)

    # Crear el payload para la API
    payload = create_payload(data)

    # Definir el tamaño del lote según los límites de la API
    batch_size = 200  # Máximo permitido por la API
    total_batches = (len(payload) + batch_size - 1) // batch_size

    # Variables para estadísticas
    total_updated = 0
    total_successful_batches = 0

    # Procesar y enviar cada lote
    for i in tqdm(range(total_batches), desc="📤 Procesando lotes"):
        batch = payload[i * batch_size:(i + 1) * batch_size]
        logging.info(f"➡️ Enviando lote {i + 1} de {total_batches} con {len(batch)} registros.")
        response = send_batch(API_KEY, batch)
        if response and response.status_code == 200:
            total_updated += len(batch)  # Incrementar por el tamaño del lote actual
            total_successful_batches += 1
        else:
            logging.error(f"⚠️ Error en el lote {i + 1}.")

        # Respetar el límite de 5 solicitudes por segundo
        time.sleep(0.2)

    # Mostrar resumen de la operación
    logging.info(f"🎉 Operación completada: {total_successful_batches}/{total_batches} lotes enviados exitosamente.")
    logging.info(f"✅ Total de perfiles actualizados: {total_updated}")

# Ejecución principal
if __name__ == "__main__":
    process_and_send()
