# 🤖 Bot de Estado de Servicios Cloud

Un bot inteligente de Telegram para monitorear el estado de los principales proveedores cloud en tiempo real.

## ✨ Características

### 🌐 Monitoreo en Tiempo Real
- **Azure** - Microsoft Cloud Services
- **GCP** - Google Cloud Platform
- **AWS** - Amazon Web Services
- **OCI** - Oracle Cloud Infrastructure

### 📊 Estadísticas Avanzadas
- Contador de comandos ejecutados
- Estadísticas por tipo de comando
- Tiempo de actividad del bot
- Tasa de éxito por proveedor
- Estadísticas diarias de uso

### ⚡ Rendimiento Optimizado
- Sistema de caché inteligente con TTL configurable
- Peticiones HTTP con reintentos automáticos
- Ejecución paralela de verificaciones
- Sesiones HTTP reutilizables
- Timeouts configurables

### 🎨 Interfaz Mejorada
- Botones inline para navegación rápida
- Emojis y formato visual atractivo
- Mensajes informativos con resúmenes
- Estados claros y fáciles de entender

## 🚀 Instalación

### Requisitos
- Python 3.8+
- Token de bot de Telegram

### Pasos de instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd BotCloud
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar el bot**
```bash
# Copiar archivo de configuración
copy env_example.txt .env

# Editar configuración
notepad .env
```

4. **Configurar token de Telegram**
Edita el archivo `.env` y añade tu token:
```env
TELEGRAM_BOT_TOKEN=tu_token_aqui
```

5. **Ejecutar el bot**
```bash
python main.py
```

## 📋 Comandos Disponibles

### Comandos Principales
- `/start` - Mensaje de bienvenida
- `/status` - Estado general de todos los proveedores
- `/help` - Mostrar ayuda
- `/stats` - Estadísticas del bot

### Comandos Específicos
- `/azure` - Estado detallado de Azure
- `/gcp` - Estado detallado de Google Cloud Platform
- `/aws` - Estado detallado de Amazon Web Services
- `/oci` - Estado detallado de Oracle Cloud Infrastructure

## ⚙️ Configuración

### Variables de Entorno

| Variable | Descripción | Por Defecto |
|----------|-------------|-------------|
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram | **Obligatorio** |
| `CACHE_DURATION` | Duración del caché en segundos | 300 (5 min) |
| `HTTP_TIMEOUT` | Timeout para peticiones HTTP | 10 segundos |
| `MAX_RETRIES` | Reintentos para peticiones HTTP | 3 |
| `LOG_LEVEL` | Nivel de logging | INFO |
| `ENABLE_STATISTICS` | Habilitar estadísticas | true |

### Ejemplo de configuración completa
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
CACHE_DURATION=300
HTTP_TIMEOUT=10
MAX_RETRIES=3
LOG_LEVEL=INFO
ENABLE_STATISTICS=true
```

## 🔧 Características Técnicas

### Sistema de Caché
- Caché por proveedor con TTL configurable
- Evita peticiones innecesarias
- Mejora el rendimiento y reduce latencia

### Manejo de Errores
- Reintentos automáticos con backoff exponencial
- Múltiples fuentes de datos por proveedor
- Fallback a estado operativo por defecto

### Estadísticas
- Registro automático de comandos
- Métricas de rendimiento por proveedor
- Estadísticas diarias y resúmenes

## 📈 Estados Posibles

- 🟢 **Operational** - Servicio funcionando normalmente
- 🔴 **Issue** - Problema detectado
- 🟡 **Investigating** - Investigando problema
- ⚪ **Unknown** - Estado desconocido

## 🛠️ Desarrollo

### Estructura del Proyecto
```
BotCloud/
├── main.py              # Punto de entrada principal
├── telegram_bot.py      # Lógica del bot de Telegram
├── cloud_status.py      # Verificación de estado cloud
├── statistics.py        # Sistema de estadísticas
├── config.py           # Configuración del bot
├── requirements.txt    # Dependencias
├── env_example.txt    # Ejemplo de configuración
└── README.md          # Documentación
```

### Agregar Nuevos Proveedores
Para agregar un nuevo proveedor:

1. Añadir método en `CloudStatusChecker`
2. Implementar parser específico
3. Actualizar comandos en `telegram_bot.py`
4. Añadir botones en la interfaz

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes problemas:
1. Verifica que Python esté instalado correctamente
2. Asegúrate de que el token de Telegram sea válido
3. Revisa los logs del bot para errores específicos
4. Ejecuta `python test_bot.py` para diagnosticar

---

**¡Disfruta monitoreando tus servicios cloud! ☁️🤖** 