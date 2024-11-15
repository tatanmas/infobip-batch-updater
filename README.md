# Infobip Batch Updater

Este proyecto es un script en Python que automatiza la actualización de perfiles en Infobip utilizando su API de Batch Update.

## ¿Qué hace este programa?

1. **Lee un archivo CSV:** Extrae los datos de perfiles, como nombres y números de teléfono.
2. **Prepara y limpia los datos:** Asegura que los caracteres especiales se manejen correctamente.
3. **Envía la información a Infobip:** Usa la API para actualizar los perfiles en lotes de hasta 200 registros.
4. **Muestra el progreso y resultados:** Podrás ver en la terminal cuántos perfiles se actualizaron con éxito y si hubo errores.

## Configuración

### 1. Clona el repositorio

Primero, clona este repositorio y navega al directorio del proyecto:

```bash
git clone https://github.com/tatanmas/infobip-batch-updater.git
cd infobip-batch-updater
```

### 2. Crea y activa un entorno virtual

Crea un entorno virtual para instalar las dependencias:

```bash
python3 -m venv venv
```

Activa el entorno virtual:

- En macOS/Linux:
  ```bash
  source venv/bin/activate
  ```
- En Windows:
  ```bash
  venv\Scripts\activate
  ```

### 3. Instala las dependencias

Con el entorno virtual activado, instala las dependencias:

```bash
pip install -r requirements.txt
```

### 4. Configura el archivo `.env`

Crea un archivo llamado `.env` en el directorio del proyecto y agrega lo siguiente:

```
API_KEY=tu_api_key
BASE_URL=https://your-infobip-base-url
CSV_FILE=data.csv
```

- **API_KEY**: Tu clave de API de Infobip.
- **BASE_URL**: La URL base de Infobip, por ejemplo: `https://198rld.api.infobip.com`.
- **CSV_FILE**: El nombre del archivo CSV que contiene los datos (asegúrate de que esté en el mismo directorio que el script).

## Ejecución

Asegúrate de que el archivo `data.csv` esté en el directorio del proyecto y luego ejecuta el script con:

```bash
python main.py
```

Los resultados y el progreso se mostrarán directamente en la terminal.

