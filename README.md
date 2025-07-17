# 🤖 Bot de Estado de Servicios Cloud

Un bot de Telegram que monitorea el estado actual de los principales proveedores de servicios cloud: **Azure**, **Google Cloud Platform (GCP)** y **Amazon Web Services (AWS)**.

## 🌟 Características

- **Monitoreo en tiempo real** del estado de servicios cloud
- **Caché inteligente** para respuestas rápidas (5 minutos por defecto)
- **Interfaz amigable** con emojis y botones inline
- **Comandos específicos** para cada proveedor
- **Logging detallado** para debugging
- **Configuración flexible** mediante variables de entorno

## 📋 Requisitos

- Python 3.8 o superior
- Token de bot de Telegram
- Conexión a internet

## 🚀 Instalación

### Opción A: Instalación Local (Recomendado para desarrollo)

1. **Clonar o descargar el proyecto:**
   ```bash
   cd BotCloud
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno:**
   ```bash
   # Copiar el archivo de ejemplo
   cp env_example.txt .env
   
   # Editar .env con tu token de bot
   nano .env
   ```

4. **Obtener token de bot de Telegram:**
   
   #### Guía paso a paso:
   
   1. **Abre Telegram** en tu teléfono o computadora
   2. **Busca @BotFather** en la barra de búsqueda de Telegram
   3. **Inicia una conversación** con BotFather haciendo clic en "Start"
   4. **Envía el comando** `/newbot`
   5. **Sigue las instrucciones**:
      - **Nombre del bot**: Escribe un nombre para tu bot (ej: "Mi Bot de Estado Cloud")
      - **Username del bot**: Escribe un nombre de usuario único que termine en "bot" (ej: "mi_estado_cloud_bot")
   6. **Copia el token** que te envía BotFather
   7. **Guarda el token** en un lugar seguro
   
   > 🔒 **Seguridad**: El token es como la contraseña de tu bot. Nunca lo compartas con nadie.

### Opción B: Instalación con Docker (Recomendado para producción)

1. **Configurar el bot:**
   ```bash
   cp env_example.txt .env
   nano .env  # Editar con tu token
   ```

2. **Construir y ejecutar:**
   ```bash
   docker-compose up -d
   ```

3. **Ver logs:**
   ```bash
   docker-compose logs -f
   ```

> 📖 **Ver [DOCKER.md](DOCKER.md) para instrucciones detalladas de Docker**

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `TELEGRAM_BOT_TOKEN` | Token de tu bot de Telegram | **Requerido** |
| `CACHE_DURATION` | Duración del caché en segundos | `300` (5 minutos) |
| `LOG_LEVEL` | Nivel de logging | `INFO` |

### Ejemplo de archivo `.env`:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
CACHE_DURATION=300
LOG_LEVEL=INFO
```

## 🎯 Uso

### Ejecutar el bot:
```bash
python main.py
```

### Comandos disponibles:

| Comando | Descripción |
|---------|-------------|
| `/start` | Mensaje de bienvenida y botones |
| `/help` | Mostrar ayuda y comandos disponibles |
| `/status` | Estado general de todos los proveedores |
| `/azure` | Estado específico de Azure |
| `/gcp` | Estado específico de Google Cloud |
| `/aws` | Estado específico de AWS |

### Interfaz de botones:
El bot también incluye botones inline para navegación rápida:
- 🌐 Estado General
- ☁️ Azure
- ☁️ GCP
- ☁️ AWS

## 📊 Estados de Servicios

| Estado | Emoji | Descripción |
|--------|-------|-------------|
| Operational | 🟢 | Servicio funcionando normalmente |
| Issue | 🔴 | Problema detectado |
| Investigating | 🟡 | Investigando problema |
| Unknown | ⚪ | Estado desconocido |

## 🏗️ Estructura del Proyecto

```
BotCloud/
├── main.py              # Punto de entrada principal
├── telegram_bot.py      # Lógica del bot de Telegram
├── cloud_status.py      # Verificación de estado de servicios cloud
├── config.py           # Configuración y variables de entorno
├── requirements.txt    # Dependencias de Python
├── env_example.txt     # Ejemplo de variables de entorno
├── .gitignore          # Archivos a ignorar en Git
├── .dockerignore       # Archivos a ignorar en Docker
├── Dockerfile          # Configuración de Docker
├── docker-compose.yml  # Orquestación de Docker
├── test_bot.py         # Script de pruebas
├── run.bat            # Script de ejecución para Windows
├── run.sh             # Script de ejecución para Linux/Mac
├── README.md          # Esta documentación
├── DOCKER.md          # Guía de Docker
├── INSTALACION_WINDOWS.md # Guía específica para Windows
├── INICIO_RAPIDO.md   # Guía de inicio rápido
└── CREAR_BOT_TELEGRAM.md # Guía para crear bot en Telegram
```

## 🔒 Seguridad

### Archivo .gitignore
El proyecto incluye un archivo `.gitignore` que protege:
- Archivos de configuración con tokens (`.env`)
- Archivos de Python compilados (`__pycache__/`)
- Entornos virtuales (`venv/`, `env/`)
- Logs y archivos temporales
- Credenciales y certificados

### Protección de tokens
- **Nunca** subas tu archivo `.env` a repositorios públicos
- **Nunca** compartas tu token de Telegram
- **Siempre** usa el archivo `.env` para configurar tokens
- El archivo `env_example.txt` es seguro de subir (no contiene tokens reales)

## 🔧 Desarrollo

### Agregar un nuevo proveedor:

1. **Modificar `cloud_status.py`:**
   - Agregar método `get_[provider]_status()`
   - Implementar parser específico `_parse_[provider]_data()`

2. **Actualizar `telegram_bot.py`:**
   - Agregar comando `/[provider]`
   - Actualizar botones inline

3. **Actualizar documentación**

### Ejemplo de implementación:
```python
async def get_new_provider_status(self) -> Dict:
    """Obtener estado del nuevo proveedor"""
    # Implementar lógica aquí
    pass

def _parse_new_provider_data(self, data: Dict) -> Dict:
    """Parsear datos del nuevo proveedor"""
    # Implementar parser aquí
    pass
```

## 🐛 Troubleshooting

### Error: "TELEGRAM_BOT_TOKEN es requerido"
- Verifica que el archivo `.env` existe
- Asegúrate de que `TELEGRAM_BOT_TOKEN` esté configurado correctamente

### Error: "Error obteniendo el estado"
- Verifica tu conexión a internet
- Algunos proveedores pueden tener limitaciones de rate limiting
- Revisa los logs para más detalles

### El bot no responde
- Verifica que el token sea válido
- Asegúrate de que el bot esté iniciado correctamente
- Revisa los logs para errores

## 📝 Logs

El bot genera logs detallados que incluyen:
- Inicio y parada del bot
- Errores de conexión
- Uso de caché
- Comandos recibidos

Para cambiar el nivel de logging, modifica `LOG_LEVEL` en el archivo `.env`.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Librería de Telegram
- [aiohttp](https://github.com/aio-libs/aiohttp) - Cliente HTTP asíncrono
- APIs oficiales de Azure, GCP y AWS para el estado de servicios

---

**¡Disfruta monitoreando tus servicios cloud! ☁️🤖** 