# 🐳 Guía de Docker - Bot de Estado Cloud

## 🎯 ¿Por qué usar Docker?

Docker te permite ejecutar el bot de manera consistente en cualquier entorno:
- ✅ **Fácil despliegue** en servidores
- ✅ **Entorno aislado** y reproducible
- ✅ **Gestión simplificada** de dependencias
- ✅ **Escalabilidad** horizontal
- ✅ **Desarrollo consistente** entre equipos

## 🚀 Despliegue Rápido con Docker

### Prerrequisitos
- Docker instalado
- Docker Compose instalado
- Token de bot de Telegram

### 1. Configurar el bot
```bash
# Copiar archivo de configuración
cp env_example.txt .env

# Editar con tu token
nano .env  # o notepad .env en Windows
```

### 2. Construir y ejecutar
```bash
# Construir imagen y ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

## 🔧 Opciones de Despliegue

### Opción A: Docker Compose (Recomendado)
```bash
# Construir y ejecutar en background
docker-compose up -d

# Ver estado
docker-compose ps

# Ver logs en tiempo real
docker-compose logs -f cloud-status-bot

# Detener y limpiar
docker-compose down
```

### Opción B: Docker directo
```bash
# Construir imagen
docker build -t cloud-status-bot .

# Ejecutar contenedor
docker run -d \
  --name cloud-status-bot \
  --restart unless-stopped \
  --env-file .env \
  cloud-status-bot

# Ver logs
docker logs -f cloud-status-bot

# Detener
docker stop cloud-status-bot
docker rm cloud-status-bot
```

### Opción C: Variables de entorno directas
```bash
# Sin archivo .env
docker run -d \
  --name cloud-status-bot \
  --restart unless-stopped \
  -e TELEGRAM_BOT_TOKEN="tu_token_aqui" \
  -e CACHE_DURATION=300 \
  -e LOG_LEVEL=INFO \
  cloud-status-bot
```

## 📊 Monitoreo y Logs

### Ver logs del contenedor
```bash
# Logs en tiempo real
docker-compose logs -f

# Últimas 100 líneas
docker-compose logs --tail=100

# Logs de un servicio específico
docker logs cloud-status-bot
```

### Health Check
El contenedor incluye un health check que verifica:
- ✅ Conexión a internet
- ✅ Acceso a la API de Telegram
- ✅ Estado del bot

### Verificar estado
```bash
# Estado del contenedor
docker-compose ps

# Información detallada
docker inspect cloud-status-bot

# Estadísticas de recursos
docker stats cloud-status-bot
```

## 🔄 Actualizaciones

### Actualizar el bot
```bash
# Detener contenedor
docker-compose down

# Reconstruir imagen
docker-compose build --no-cache

# Ejecutar nueva versión
docker-compose up -d
```

### Actualizar solo el código
```bash
# Reconstruir sin caché
docker-compose build --no-cache cloud-status-bot

# Reiniciar servicio
docker-compose restart cloud-status-bot
```

## 🛠️ Desarrollo con Docker

### Modo desarrollo
```bash
# Ejecutar en modo interactivo
docker-compose run --rm cloud-status-bot python test_bot.py

# Entrar al contenedor
docker-compose exec cloud-status-bot bash

# Ejecutar comandos específicos
docker-compose exec cloud-status-bot python -c "print('Hello from container!')"
```

### Debugging
```bash
# Ver logs detallados
docker-compose logs -f --tail=50

# Verificar configuración
docker-compose exec cloud-status-bot cat .env

# Verificar dependencias
docker-compose exec cloud-status-bot pip list
```

## 🌐 Despliegue en Producción

### Variables de entorno recomendadas
```env
TELEGRAM_BOT_TOKEN=tu_token_aqui
CACHE_DURATION=300
LOG_LEVEL=INFO
```

### Configuración de red
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  cloud-status-bot:
    build: .
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
      - CACHE_DURATION=300
      - LOG_LEVEL=INFO
    networks:
      - bot-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  bot-network:
    driver: bridge
```

### Comandos de producción
```bash
# Desplegar en producción
docker-compose -f docker-compose.prod.yml up -d

# Verificar estado
docker-compose -f docker-compose.prod.yml ps

# Backup de logs
docker-compose -f docker-compose.prod.yml logs > bot-logs-$(date +%Y%m%d).log
```

## 🔒 Seguridad

### Buenas prácticas
- ✅ **Nunca** incluir tokens en el Dockerfile
- ✅ **Usar** archivos `.env` o variables de entorno
- ✅ **Ejecutar** como usuario no root (ya configurado)
- ✅ **Limitar** recursos del contenedor
- ✅ **Actualizar** regularmente la imagen base

### Configuración de seguridad
```yaml
# docker-compose.secure.yml
version: '3.8'
services:
  cloud-status-bot:
    build: .
    restart: unless-stopped
    environment:
      - TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    networks:
      - bot-network
```

## 🐛 Troubleshooting

### Problemas comunes

#### Error: "TELEGRAM_BOT_TOKEN es requerido"
```bash
# Verificar variables de entorno
docker-compose exec cloud-status-bot env | grep TELEGRAM

# Verificar archivo .env
docker-compose exec cloud-status-bot cat .env
```

#### Error: "ModuleNotFoundError"
```bash
# Reconstruir imagen
docker-compose build --no-cache

# Verificar dependencias
docker-compose exec cloud-status-bot pip list
```

#### El bot no responde
```bash
# Verificar logs
docker-compose logs -f

# Verificar conectividad
docker-compose exec cloud-status-bot python -c "import requests; print(requests.get('https://api.telegram.org').status_code)"
```

#### Contenedor se reinicia constantemente
```bash
# Ver logs de error
docker-compose logs --tail=50

# Verificar configuración
docker-compose config
```

## 📝 Comandos Útiles

```bash
# Construir imagen
docker build -t cloud-status-bot .

# Ejecutar con Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Limpiar imágenes no usadas
docker system prune -a

# Ver estadísticas
docker stats

# Backup de configuración
docker cp cloud-status-bot:/app/.env ./backup.env
```

---

**¡Tu bot está listo para ejecutarse en cualquier entorno con Docker! 🐳🤖** 