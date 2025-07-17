# 🪟 Guía de Instalación para Windows

## 📋 Requisitos Previos

### 1. Instalar Python

**Opción A: Desde Microsoft Store (Recomendado)**
1. Abre Microsoft Store
2. Busca "Python 3.11" o "Python 3.12"
3. Haz clic en "Obtener" o "Instalar"
4. Espera a que se complete la instalación

**Opción B: Desde python.org**
1. Ve a [python.org/downloads](https://python.org/downloads)
2. Descarga la última versión de Python para Windows
3. Ejecuta el instalador
4. **IMPORTANTE**: Marca la casilla "Add Python to PATH"
5. Haz clic en "Install Now"

### 2. Verificar la instalación
Abre PowerShell o CMD y ejecuta:
```powershell
python --version
```
Deberías ver algo como: `Python 3.11.5`

## 🚀 Instalación del Bot

### 1. Navegar al directorio
```powershell
cd "C:\Users\Sergi\Documents\Apunts\Terraform\BotCloud"
```

### 2. Instalar dependencias
```powershell
pip install -r requirements.txt
```

### 3. Configurar el bot

#### Paso 1: Copiar archivo de configuración
```powershell
copy env_example.txt .env
```

#### Paso 2: Editar configuración
```powershell
notepad .env
```

#### Paso 3: Configurar el token
En el archivo `.env`, busca esta línea:
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

Y reemplázala con tu token real:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

> 💡 **Ejemplo**: Si tu token es `9876543210:XYZabcDEFghiJKLmnoPQRstuVWXyz`, la línea debería quedar:
> ```env
> TELEGRAM_BOT_TOKEN=9876543210:XYZabcDEFghiJKLmnoPQRstuVWXyz
> ```

**Guarda el archivo** y cierra el editor.

### 4. Obtener token de Telegram

#### Guía paso a paso:

1. **Abre Telegram** en tu teléfono o computadora

2. **Busca @BotFather** en la barra de búsqueda de Telegram

3. **Inicia una conversación** con BotFather:
   - Haz clic en "Start" o envía `/start`

4. **Crea tu bot** enviando el comando `/newbot`

5. **Configura tu bot**:
   - **Nombre del bot**: Escribe un nombre descriptivo (ej: "Mi Bot de Estado Cloud")
   - **Username del bot**: Escribe un nombre de usuario único que termine en "bot" (ej: "mi_estado_cloud_bot")

6. **Recibe tu token**: BotFather te enviará un mensaje como este:
   ```
   Use this token to access the HTTP API:
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   
   Keep your token secure and store it safely, it can be used by anyone to control your bot.
   ```

7. **Guarda el token** en un lugar seguro

> 🔒 **Seguridad**: El token es como la contraseña de tu bot. Nunca lo compartas con nadie ni lo subas a repositorios públicos.

## 🎯 Ejecutar el Bot

### Opción A: Script automático (Recomendado)
```powershell
.\run.bat
```

### Opción B: Manual
```powershell
python main.py
```

### Opción C: Pruebas
```powershell
python test_bot.py
```

## 🔧 Solución de Problemas

### Error: "python no se reconoce"
- Python no está en el PATH
- Reinstala Python marcando "Add Python to PATH"
- O reinicia tu terminal después de instalar

### Error: "pip no se reconoce"
- Instala pip: `python -m ensurepip --upgrade`
- O usa: `python -m pip install -r requirements.txt`

### Error: "TELEGRAM_BOT_TOKEN es requerido"
- Verifica que el archivo `.env` existe
- Asegúrate de que el token esté correctamente configurado

### Error: "ModuleNotFoundError"
- Instala las dependencias: `pip install -r requirements.txt`

## 📱 Usar el Bot

1. **Inicia el bot** con `run.bat`
2. **Abre Telegram** y busca tu bot
3. **Envía `/start`** para comenzar
4. **Usa los comandos**:
   - `/status` - Estado general
   - `/azure` - Estado de Azure
   - `/gcp` - Estado de Google Cloud
   - `/aws` - Estado de AWS

## 🛠️ Comandos Útiles

```powershell
# Verificar Python
python --version

# Verificar pip
pip --version

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar pruebas
python test_bot.py

# Ejecutar bot
python main.py

# Detener bot
Ctrl+C
```

## 📞 Soporte

Si tienes problemas:
1. Ejecuta `python test_bot.py` para diagnosticar
2. Verifica que Python esté instalado correctamente
3. Asegúrate de que el token de Telegram sea válido
4. Revisa los logs del bot para errores específicos

---

**¡Disfruta monitoreando tus servicios cloud! ☁️🤖** 