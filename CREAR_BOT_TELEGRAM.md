# 🤖 Guía Completa: Crear Bot en Telegram

## 📱 Paso a Paso para Crear tu Bot

### 1. Abrir Telegram
- **En tu teléfono**: Abre la app de Telegram
- **En tu computadora**: Abre Telegram Web o la aplicación de escritorio

### 2. Buscar BotFather
- En la barra de búsqueda de Telegram, escribe: `@BotFather`
- Haz clic en el resultado que aparece

### 3. Iniciar conversación
- Haz clic en el botón **"Start"** o envía `/start`
- BotFather te dará la bienvenida y te mostrará los comandos disponibles

### 4. Crear tu bot
- Envía el comando: `/newbot`
- BotFather te preguntará el **nombre** de tu bot

### 5. Configurar el nombre
- Escribe un nombre descriptivo, por ejemplo:
  - "Mi Bot de Estado Cloud"
  - "Cloud Status Monitor"
  - "Estado de Servicios Cloud"
- **Presiona Enter**

### 6. Configurar el username
- Ahora BotFather te pedirá el **username** del bot
- Debe ser único y terminar en "bot"
- Ejemplos válidos:
  - `mi_estado_cloud_bot`
  - `cloud_status_monitor_bot`
  - `sergi_cloud_bot`
- **Presiona Enter**

### 7. Recibir tu token
- Si el username está disponible, BotFather te enviará un mensaje como este:

```
Done! Congratulations on your new bot. You will find it at t.me/tu_username_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

Keep your token secure and store it safely, it can be used by anyone to control your bot.
```

### 8. Guardar el token
- **Copia el token** (la línea que empieza con números)
- **Guárdalo en un lugar seguro** - lo necesitarás para configurar el bot

## 🔒 Seguridad del Token

### ⚠️ IMPORTANTE
- **El token es como la contraseña de tu bot**
- **Nunca lo compartas con nadie**
- **Nunca lo subas a repositorios públicos**
- **Si alguien tiene tu token, puede controlar tu bot**

### 🛡️ Buenas prácticas
- Guarda el token en un gestor de contraseñas
- No lo envíes por mensajes de texto o email
- Usa el archivo `.env` para configurarlo en el código
- El archivo `.gitignore` ya está configurado para proteger `.env`

## 📋 Configurar el Bot

### Opcional: Personalizar tu bot
Una vez creado, puedes personalizarlo con estos comandos:

- `/setdescription` - Agregar descripción del bot
- `/setabouttext` - Agregar información "Acerca de"
- `/setuserpic` - Cambiar foto de perfil
- `/setcommands` - Configurar comandos disponibles

### Ejemplo de comandos para configurar:
```
start - Iniciar el bot y ver opciones
help - Mostrar ayuda y comandos disponibles
status - Estado general de todos los proveedores cloud
azure - Estado específico de Azure
gcp - Estado específico de Google Cloud Platform
aws - Estado específico de Amazon Web Services
```

## 🎯 Usar tu Bot

### 1. Buscar tu bot
- En Telegram, busca el username que creaste (ej: `@mi_estado_cloud_bot`)
- O usa el enlace que te dio BotFather: `t.me/tu_username_bot`

### 2. Iniciar conversación
- Haz clic en **"Start"** o envía `/start`
- Tu bot debería responder con el mensaje de bienvenida

### 3. Probar comandos
- Envía `/status` para ver el estado de los servicios cloud
- Usa los botones inline para navegar
- Prueba los comandos específicos: `/azure`, `/gcp`, `/aws`

## 🔧 Solución de Problemas

### Error: "Username already taken"
- El username que elegiste ya está en uso
- Prueba con otro username (ej: `mi_estado_cloud_2024_bot`)

### Error: "Username must end with 'bot'"
- El username debe terminar exactamente en "bot"
- Ejemplo correcto: `mi_bot_estado_bot`

### El bot no responde
- Verifica que el token esté correctamente configurado en `.env`
- Asegúrate de que el bot esté ejecutándose (`python main.py`)
- Revisa los logs para errores

### Token perdido o comprometido
- Si pierdes el token o crees que se ha comprometido:
  1. Habla con @BotFather
  2. Envía `/mybots`
  3. Selecciona tu bot
  4. Envía `/revoke`
  5. Crea un nuevo bot con `/newbot`

## 📞 Comandos útiles de BotFather

- `/mybots` - Ver tus bots
- `/revoke` - Revocar token de un bot
- `/deletebot` - Eliminar un bot
- `/help` - Ver todos los comandos disponibles

---

**¡Ahora tienes todo lo necesario para crear y configurar tu bot de Telegram! 🤖✨** 