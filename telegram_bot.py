import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from cloud_status import CloudStatusChecker
from config import Config
from datetime import datetime

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, Config.LOG_LEVEL)
)
logger = logging.getLogger(__name__)

class CloudStatusBot:
    """Bot de Telegram para monitorear el estado de servicios cloud"""
    
    def __init__(self):
        self.status_checker = CloudStatusChecker()
        self.application = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start - Mensaje de bienvenida"""
        welcome_message = """
🤖 *Bot de Estado de Servicios Cloud*

¡Hola! Soy tu asistente para monitorear el estado de los principales proveedores cloud:

☁️ *Azure* - Microsoft Cloud Services
☁️ *GCP* - Google Cloud Platform  
☁️ *AWS* - Amazon Web Services

*Comandos disponibles:*
/status - Estado general de todos los proveedores
/azure - Estado específico de Azure
/gcp - Estado específico de Google Cloud
/aws - Estado específico de AWS
/help - Mostrar esta ayuda
        """
        
        keyboard = [
            [InlineKeyboardButton("🌐 Estado General", callback_data="status_all")],
            [InlineKeyboardButton("☁️ Azure", callback_data="status_azure")],
            [InlineKeyboardButton("☁️ GCP", callback_data="status_gcp")],
            [InlineKeyboardButton("☁️ AWS", callback_data="status_aws")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help - Mostrar ayuda"""
        help_message = """
📚 *Comandos del Bot*

*Comandos principales:*
/start - Mensaje de bienvenida
/status - Estado de todos los proveedores cloud
/help - Mostrar esta ayuda

*Comandos específicos:*
/azure - Estado detallado de Azure
/gcp - Estado detallado de Google Cloud Platform
/aws - Estado detallado de Amazon Web Services

*Estados posibles:*
🟢 Operational - Servicio funcionando normalmente
🔴 Issue - Problema detectado
🟡 Investigating - Investigando problema
⚪ Unknown - Estado desconocido
        """
        
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status - Estado general de todos los proveedores"""
        await self._send_status_message(update, context, "all")
    
    async def azure_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /azure - Estado específico de Azure"""
        await self._send_status_message(update, context, "azure")
    
    async def gcp_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /gcp - Estado específico de GCP"""
        await self._send_status_message(update, context, "gcp")
    
    async def aws_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /aws - Estado específico de AWS"""
        await self._send_status_message(update, context, "aws")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar callbacks de botones inline"""
        query = update.callback_query
        await query.answer()
        
        if query.data.startswith("status_"):
            provider = query.data.replace("status_", "")
            await self._send_status_message(update, context, provider, is_callback=True)
    
    async def _send_status_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, provider: str, is_callback: bool = False):
        """Enviar mensaje de estado"""
        loading_message = "🔄 Obteniendo estado de los servicios cloud..."
        
        if is_callback:
            await update.callback_query.edit_message_text(loading_message)
        else:
            message = await update.message.reply_text(loading_message)
        
        try:
            if provider == "all":
                status_data = await self.status_checker.get_all_status()
                response_text = self._format_all_status(status_data)
            else:
                status_data = await self.status_checker.get_provider_status(provider)
                response_text = self._format_provider_status(status_data)
            
            keyboard = [
                [InlineKeyboardButton("🌐 General", callback_data="status_all")],
                [InlineKeyboardButton("☁️ Azure", callback_data="status_azure")],
                [InlineKeyboardButton("☁️ GCP", callback_data="status_gcp")],
                [InlineKeyboardButton("☁️ AWS", callback_data="status_aws")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if is_callback:
                await update.callback_query.edit_message_text(
                    response_text,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
            else:
                await message.edit_text(
                    response_text,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )
                
        except Exception as e:
            error_message = f"❌ Error obteniendo el estado: {str(e)}"
            if is_callback:
                await update.callback_query.edit_message_text(error_message)
            else:
                await message.edit_text(error_message)
    
    def _format_all_status(self, status_data: dict) -> str:
        """Formatear estado de todos los proveedores"""
        message = "🌐 *Estado General de Servicios Cloud*\n\n"
        message += f"📅 *Actualizado:* {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        
        for provider, data in status_data.items():
            if "error" in data:
                message += f"❌ *{provider.upper()}*: Error - {data.get('message', 'Error desconocido')}\n\n"
            else:
                status_emoji = "🟢" if data.get('overall_status') == 'Operational' else "🔴"
                message += f"{status_emoji} *{data.get('provider', provider.upper())}*: {data.get('overall_status', 'Unknown')}\n\n"
        
        message += "💡 *Usa los botones para ver detalles específicos*"
        return message
    
    def _format_provider_status(self, data: dict) -> str:
        """Formatear estado de un proveedor específico"""
        if "error" in data:
            return f"❌ *Error:* {data.get('message', 'Error desconocido')}"
        
        provider_name = data.get('provider', 'Unknown')
        overall_status = data.get('overall_status', 'Unknown')
        services = data.get('services', [])
        
        status_emoji = "🟢" if overall_status == 'Operational' else "🔴"
        
        message = f"{status_emoji} *{provider_name}*\n"
        message += f"📊 *Estado General:* {overall_status}\n"
        message += f"📅 *Actualizado:* {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
        
        if services:
            message += "📋 *Servicios:*\n"
            for service in services:
                service_status = service.get('status', 'Unknown')
                service_emoji = "🟢" if service_status == 'Operational' else "🔴"
                service_name = service.get('name', 'Unknown')
                
                message += f"{service_emoji} *{service_name}*: {service_status}\n"
        else:
            message += "📋 No hay información de servicios disponible\n"
        
        return message
    
    def run(self):
        """Ejecutar el bot"""
        try:
            Config.validate()
            self.application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
            
            self.application.add_handler(CommandHandler("start", self.start_command))
            self.application.add_handler(CommandHandler("help", self.help_command))
            self.application.add_handler(CommandHandler("status", self.status_command))
            self.application.add_handler(CommandHandler("azure", self.azure_command))
            self.application.add_handler(CommandHandler("gcp", self.gcp_command))
            self.application.add_handler(CommandHandler("aws", self.aws_command))
            self.application.add_handler(CallbackQueryHandler(self.button_callback))
            
            logger.info("Bot iniciado correctamente")
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except Exception as e:
            logger.error(f"Error iniciando el bot: {e}")
            raise

if __name__ == "__main__":
    bot = CloudStatusBot()
    bot.run() 