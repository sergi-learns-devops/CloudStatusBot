# ⚡ Inicio Rápido - Bot de Estado Cloud

## 🎯 ¿Qué hace este bot?

Este bot de Telegram te permite consultar el estado actual de los servicios cloud de:
- ☁️ **Azure** (Microsoft)
- ☁️ **GCP** (Google Cloud Platform)  
- ☁️ **AWS** (Amazon Web Services)

## 🚀 Pasos para usar (5 minutos)

### 1. Instalar Python
```powershell
# Abre Microsoft Store y busca "Python 3.11"
# O descarga desde python.org (marca "Add to PATH")
```

### 2. Configurar el bot
```powershell
# Navega al directorio
cd "C:\Users\Sergi\Documents\Apunts\Terraform\BotCloud"

# Instala dependencias
pip install -r requirements.txt

# Copia configuración
copy env_example.txt .env
```

### 3. Obtener token de Telegram

#### Paso a paso detallado:

1. **Abre Telegram** en tu teléfono o computadora

2. **Busca @BotFather** en la barra de búsqueda de Telegram

3. **Inicia una conversación** con BotFather haciendo clic en "Start"

4. **Envía el comando** `/newbot`

5. **Sigue las instrucciones**:
   - **Nombre del bot**: Escribe un nombre para tu bot (ej: "Mi Bot de Estado Cloud")
   - **Username del bot**: Escribe un nombre de usuario único que termine en "bot" (ej: "mi_estado_cloud_bot")

6. **Copia el token**: BotFather te enviará un mensaje como este:
   ```
   Use this token to access the HTTP API:
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   
   Keep your token secure and store it safely, it can be used by anyone to control your bot.
   ```

7. **Guarda el token** en un lugar seguro - lo necesitarás para el siguiente paso

> ⚠️ **IMPORTANTE**: Nunca compartas tu token con nadie. Es como la contraseña de tu bot.

### 4. Configurar token

```powershell
# Edita el archivo .env
notepad .env
```

**En el archivo .env, busca esta línea:**
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

**Y reemplázala con tu token real:**
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

> 💡 **Ejemplo**: Si tu token es `9876543210:XYZabcDEFghiJKLmnoPQRstuVWXyz`, la línea debería quedar:
> ```env
> TELEGRAM_BOT_TOKEN=9876543210:XYZabcDEFghiJKLmnoPQRstuVWXyz
> ```

**Guarda el archivo** y cierra el editor.

### 5. Ejecutar
```powershell
# Opción fácil (recomendado)
.\run.bat

# O manual
python main.py
```

## 📱 Comandos del Bot

| Comando | Descripción |
|---------|-------------|
| `/start` | Bienvenida y botones |
| `/status` | Estado de todos los proveedores |
| `/azure` | Solo Azure |
| `/gcp` | Solo Google Cloud |
| `/aws` | Solo AWS |
| `/help` | Ayuda |

## 🎨 Ejemplo de uso

```
🤖 Bot de Estado de Servicios Cloud

🌐 Estado General de Servicios Cloud

📅 Actualizado: 15/12/2024 14:30:25

🟢 Azure: Operational

🟢 Google Cloud Platform: Operational

🟢 AWS: Operational

💡 Usa los botones para ver detalles específicos
```

## 🔧 Si algo no funciona

### Error: "python no se reconoce"
- Instala Python desde Microsoft Store
- Marca "Add to PATH" durante la instalación

### Error: "TELEGRAM_BOT_TOKEN es requerido"
- Verifica que el archivo `.env` existe
- Asegúrate de que el token esté correcto

### Error: "ModuleNotFoundError"
- Ejecuta: `pip install -r requirements.txt`

### El bot no responde
- Verifica que el token sea válido
- Revisa que el bot esté ejecutándose

## 📞 Pruebas

Para verificar que todo funciona:
```powershell
python test_bot.py
```

## 🎉 ¡Listo!

Una vez configurado, podrás:
- ✅ Consultar el estado de servicios cloud en tiempo real
- ✅ Recibir notificaciones con emojis y formato claro
- ✅ Navegar fácilmente con botones inline
- ✅ Tener respuestas rápidas con caché inteligente

---

**¡Disfruta monitoreando tus servicios cloud! ☁️🤖** 