# API Inteligente de Reseñas de Negocio RD

API RESTful desarrollada con **FastAPI**, **SQLite** y la **SDK Oficial de Google Gemini (`google-genai`)** para la gestión, clasificación automatizada de sentimientos y síntesis analítica de opiniones de clientes.

## Descripción del Proyecto

Esta API permite a los propietarios de negocios locales recopilar, consultar, actualizar y eliminar reseñas de sus clientes. Aprovecha las capacidades de la Inteligencia Artificial Generativa de Google Gemini (`gemini-2.0-flash`) para:

1. **Analizar automáticamente el sentimiento** (`Positivo`, `Neutral` o `Negativo`) de cada comentario ingresado en español en tiempo real.
2. **Generar un resumen ejecutivo** de la opinión general de los usuarios, destacando los puntos fuertes y las áreas de mejora del negocio.

## tecnologías Utilizadas

* **Lenguaje:** Python 3.10+
* **Framework Web:** FastAPI
* **Servidor ASGI:** Uvicorn
* **Base de Datos:** SQLite
* **ORM:** SQLAlchemy
* **Validación de Datos:** Pydantic (v2)
* **Inteligencia Artificial:** SDK oficial `google-genai` (Modelo `gemini-2.0-flash`)
* **Gestión de Entorno:** `python-dotenv`

## Estructura del Proyecto

```text
proyecto_resenas/
├── capturas/               # Evidencias y capturas de pantalla de la API
├── .env                    # Variables de entorno (API Key de Gemini)
├── .env.example            # Plantilla de variables de entorno sin datos sensibles
├── .gitignore              # Archivo de exclusión para Git (ignora .env y venv)
├── database.py             # Configuración de la conexión y sesión SQLite
├── main.py                 # Rutas/endpoints de FastAPI (CRUD y resumen)
├── models.py               # Modelo de la tabla 'resenas' con SQLAlchemy
├── pyproject.toml          # Configuración del paquete y gestor de dependencias
├── README.md               # Documentación general del proyecto
├── requirements.txt        # Librerías necesarias para el entorno
├── schemas.py              # Esquemas de validación de datos con Pydantic
└── services.py             # Integración y prompts con la IA de Google Gemini
```

## Tabla de Endpoints

| Método | Ruta | Descripción | Estado HTTP |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Mensaje de bienvenida e inicio de la API. | `200 OK` |
| `POST` | `/resenas/` | Crea una nueva reseña y analiza automáticamente su sentimiento con Gemini. | `201 Created` |
| `GET` | `/resenas/` | Obtiene el listado de todas las reseñas almacenadas en la base de datos. | `200 OK` |
| `GET` | `/resenas/resumen` | Sintetiza en un reporte breve la opinión global de los clientes mediante IA. | `200 OK` |
| `PUT` | `/resenas/{resena_id}` | Actualiza una reseña existente (recalcula el sentimiento si cambia el comentario). | `200 OK` |
| `DELETE` | `/resenas/{resena_id}` | Elimina una reseña específica de la base de datos por su ID. | `200 OK` |

## Manejo de Errores

La API está diseñada para manejar respuestas HTTP estandarizadas frente a excepciones comunes:

* **`404 Not Found`**: Se devuelve cuando se intenta consultar, actualizar (`PUT`) o eliminar (`DELETE`) una reseña cuyo `ID` no existe en la base de datos SQLite.
* **`422 Unprocessable Entity`**: Proporcionado automáticamente por FastAPI y Pydantic al recibir datos inválidos en el cuerpo de la petición (por ejemplo, si faltan campos obligatorios o la calificación no es un número entero válido dentro del rango 1-5).

## Seguridad Básica y Buenas Prácticas

1. **Protección de Credenciales:** La `GEMINI_API_KEY` se carga mediante variables de entorno a través del paquete `python-dotenv` y **nunca está expuesta en el código fuente**.
2. **Control de Versiones Seguras:** El archivo `.env` está incluido dentro del `.gitignore` para evitar filtraciones accidentales a repositorios públicos. Se provee un archivo `.env.example` en el repositorio como referencia estándar.
3. **Datos de prueba:** El proyecto utiliza exclusivamente datos e identidades ficticias para realizar las pruebas de funcionalidad e integración de la IA.

---

## Requisitos Previos e Instalación

### 1. Clonar o descargar el repositorio
Asegúrate de tener el código del proyecto en tu equipo local y abrir la carpeta en tu editor de código (por ejemplo, VS Code).

### 2. Crear y activar el entorno virtual
```bash
# Crear el entorno virtual
python -m venv venv

# En Windows (PowerShell / Command Prompt):
venv\Scripts\activate

# En macOS / Linux:
source venv/bin/activate
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```
*(O si utilizas `uv`: `uv pip install -r requirements.txt`)*

### 4. Configurar la clave de la API de Gemini
Copia el archivo de plantilla `.env.example` para crear tu archivo `.env`:

```bash
cp .env.example .env
```

Abre el archivo **`.env`** e incluye tu clave privada de Google AI Studio:

```env
GEMINI_API_KEY=tu_api_key_aqui
```

> **Nota:** Si no dispones de una API Key, puedes obtenerla de forma gratuita desde [Google AI Studio](https://aistudio.google.com/app/apikey).

---

##  Instrucciones de Ejecución

1. Con el entorno virtual activado y las dependencias instaladas, ejecuta el servidor ASGI:
   ```bash
   uvicorn main:app --reload
   ```

2. Abre tu navegador web e ingresa a la documentación interactiva provista por Swagger UI:
   * **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   * **ReDoc (Alternativa):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

3. Desde Swagger UI podrás probar la creación (`POST`), consulta (`GET`), actualización (`PUT`) y eliminación (`DELETE`) de reseñas, así como solicitar el resumen automatizado por IA (`GET /resenas/resumen`).
