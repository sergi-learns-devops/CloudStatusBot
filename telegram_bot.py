import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from cloud_status import CloudStatusChecker
from config import Config
from statistics import BotStatistics
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
        self.stats = BotStatistics() if Config.ENABLE_STATISTICS else None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start - Mensaje de bienvenida"""
        if self.stats:
            self.stats.record_command("start", update.effective_user.id)
        
        welcome_message = """
🤖 *Bot de Estado de Servicios Cloud*

¡Hola! Soy tu asistente inteligente para monitorear el estado de los principales proveedores cloud en tiempo real.

☁️ *Proveedores soportados:*
• **Azure** - Microsoft Cloud Services
• **GCP** - Google Cloud Platform  
• **AWS** - Amazon Web Services
• **OCI** - Oracle Cloud Infrastructure

📊 *Comandos disponibles:*
/start - Mensaje de bienvenida
/status - Estado general de todos los proveedores
/azure - Estado específico de Azure
/gcp - Estado específico de Google Cloud
/aws - Estado específico de Amazon Web Services
/oci - Estado específico de Oracle Cloud
/stats - Estadísticas del bot
/help - Mostrar esta ayuda

💡 *Usa los botones para navegación rápida*
        """
        
        keyboard = [
            [InlineKeyboardButton("🌐 Estado General", callback_data="status_all")],
            [InlineKeyboardButton("☁️ Azure", callback_data="status_azure")],
            [InlineKeyboardButton("☁️ GCP", callback_data="status_gcp")],
            [InlineKeyboardButton("☁️ AWS", callback_data="status_aws")],
            [InlineKeyboardButton("☁️ OCI", callback_data="status_oci")],
            [InlineKeyboardButton("📊 Estadísticas", callback_data="show_stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help - Mostrar ayuda"""
        if self.stats:
            self.stats.record_command("help", update.effective_user.id)
        
        help_message = """
📚 *Comandos del Bot*

*Comandos principales:*
/start - Mensaje de bienvenida
/status - Estado de todos los proveedores cloud
/stats - Estadísticas del bot
/help - Mostrar esta ayuda

*Comandos específicos:*
/azure - Estado detallado de Azure
/gcp - Estado detallado de Google Cloud Platform
/aws - Estado detallado de Amazon Web Services
/oci - Estado detallado de Oracle Cloud Infrastructure

*Estados posibles:*
🟢 **Operational** - Servicio funcionando normalmente
🔴 **Issue** - Problema detectado
🟡 **Investigating** - Investigando problema
⚪ **Unknown** - Estado desconocido

💡 *Consejos:*
• Los datos se actualizan cada 5 minutos
• Usa los botones para navegación rápida
• El bot registra estadísticas de uso
        """
        
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /stats - Mostrar estadísticas del bot"""
        if not self.stats:
            await update.message.reply_text("❌ Las estadísticas están deshabilitadas")
            return
        
        self.stats.record_command("stats", update.effective_user.id)
        stats_message = self.stats.get_stats_summary()
        
        keyboard = [
            [InlineKeyboardButton("📅 Últimos 7 días", callback_data="daily_stats")],
            [InlineKeyboardButton("🔙 Volver", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(stats_message, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status - Estado general de todos los proveedores"""
        if self.stats:
            self.stats.record_command("status", update.effective_user.id)
        await self._send_status_message(update, context, "all")
    
    async def azure_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /azure - Estado específico de Azure"""
        if self.stats:
            self.stats.record_command("azure", update.effective_user.id)
        await self._send_status_message(update, context, "azure")
    
    async def gcp_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /gcp - Estado específico de GCP"""
        if self.stats:
            self.stats.record_command("gcp", update.effective_user.id)
        await self._send_status_message(update, context, "gcp")
    
    async def aws_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /aws - Estado específico de AWS"""
        if self.stats:
            self.stats.record_command("aws", update.effective_user.id)
        await self._send_status_message(update, context, "aws")
    
    async def oci_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /oci - Estado específico de OCI"""
        if self.stats:
            self.stats.record_command("oci", update.effective_user.id)
        await self._send_status_message(update, context, "oci")
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manejar callbacks de botones inline"""
        query = update.callback_query
        await query.answer()
        
        if query.data.startswith("status_"):
            provider = query.data.replace("status_", "")
            if self.stats:
                self.stats.record_command(f"button_{provider}", query.from_user.id)
            await self._send_status_message(update, context, provider, is_callback=True)
        
        elif query.data == "show_stats":
            if self.stats:
                self.stats.record_command("button_stats", query.from_user.id)
                stats_message = self.stats.get_stats_summary()
                
                keyboard = [
                    [InlineKeyboardButton("📅 Últimos 7 días", callback_data="daily_stats")],
                    [InlineKeyboardButton("🔙 Volver", callback_data="back_to_main")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(stats_message, parse_mode='Markdown', reply_markup=reply_markup)
        
        elif query.data == "daily_stats":
            if self.stats:
                self.stats.record_command("button_daily_stats", query.from_user.id)
                daily_stats = self.stats.get_daily_stats()
                
                keyboard = [
                    [InlineKeyboardButton("📊 Resumen", callback_data="show_stats")],
                    [InlineKeyboardButton("🔙 Volver", callback_data="back_to_main")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(daily_stats, parse_mode='Markdown', reply_markup=reply_markup)
        
        elif query.data == "back_to_main":
            # Crear un mensaje de bienvenida para el callback
            if self.stats:
                self.stats.record_command("button_back_to_main", query.from_user.id)
            
            welcome_message = """
🤖 *Bot de Estado de Servicios Cloud*

¡Hola! Soy tu asistente inteligente para monitorear el estado de los principales proveedores cloud en tiempo real.

☁️ *Proveedores soportados:*
• **Azure** - Microsoft Cloud Services
• **GCP** - Google Cloud Platform  
• **AWS** - Amazon Web Services
• **OCI** - Oracle Cloud Infrastructure

📊 *Comandos disponibles:*
/start - Mensaje de bienvenida
/status - Estado general de todos los proveedores
/azure - Estado específico de Azure
/gcp - Estado específico de Google Cloud
/aws - Estado específico de Amazon Web Services
/oci - Estado específico de Oracle Cloud
/stats - Estadísticas del bot
/help - Mostrar esta ayuda

💡 *Usa los botones para navegación rápida*
        """
            
            keyboard = [
                [InlineKeyboardButton("🌐 Estado General", callback_data="status_all")],
                [InlineKeyboardButton("☁️ Azure", callback_data="status_azure")],
                [InlineKeyboardButton("☁️ GCP", callback_data="status_gcp")],
                [InlineKeyboardButton("☁️ AWS", callback_data="status_aws")],
                [InlineKeyboardButton("☁️ OCI", callback_data="status_oci")],
                [InlineKeyboardButton("📊 Estadísticas", callback_data="show_stats")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                welcome_message,
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
    
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
                
                # Registrar estadísticas de verificación
                if self.stats:
                    success = not status_data.get("error", False)
                    self.stats.record_provider_check(provider, success)
            
            keyboard = [
                [InlineKeyboardButton("🌐 General", callback_data="status_all")],
                [InlineKeyboardButton("☁️ Azure", callback_data="status_azure")],
                [InlineKeyboardButton("☁️ GCP", callback_data="status_gcp")],
                [InlineKeyboardButton("☁️ AWS", callback_data="status_aws")],
                [InlineKeyboardButton("☁️ OCI", callback_data="status_oci")],
                [InlineKeyboardButton("📊 Estadísticas", callback_data="show_stats")]
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
        message += f"📅 *Actualizado:* {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        message += f"⏱️ *Caché:* {Config.CACHE_DURATION}s\n\n"
        
        operational_count = 0
        total_count = len(status_data)
        
        for provider, data in status_data.items():
            if data.get("error", False):
                message += f"❌ *{provider.upper()}*: Error - {data.get('message', 'Error desconocido')}\n\n"
            else:
                status = data.get('overall_status', 'Unknown')
                if status == 'Operational':
                    status_emoji = "🟢"
                    operational_count += 1
                elif status == 'Issues Detected':
                    status_emoji = "🔴"
                else:
                    status_emoji = "⚪"
                
                message += f"{status_emoji} *{data.get('provider', provider.upper())}*: {status}\n\n"
        
        # Resumen general
        if operational_count == total_count:
            message += "🎉 *Todos los servicios están operativos*\n\n"
        elif operational_count > 0:
            message += f"⚠️ *{operational_count}/{total_count} servicios operativos*\n\n"
        else:
            message += "🚨 *Todos los servicios tienen problemas*\n\n"
        
        message += "💡 *Usa los botones para ver detalles específicos*"
        return message
    
    def _format_provider_status(self, data: dict) -> str:
        """Formatear estado de un proveedor específico"""
        if data.get("error", False):
            return f"❌ *Error:* {data.get('message', 'Error desconocido')}"
        
        provider_name = data.get('provider', 'Unknown')
        overall_status = data.get('overall_status', 'Unknown')
        services = data.get('services', [])
        note = data.get('note', '')
        
        if overall_status == 'Operational':
            status_emoji = "🟢"
            status_text = "**Operativo**"
        elif overall_status == 'Issues Detected':
            status_emoji = "🔴"
            status_text = "**Problemas Detectados**"
        else:
            status_emoji = "⚪"
            status_text = f"**{overall_status}**"
        
        message = f"{status_emoji} *{provider_name}*\n"
        message += f"📊 *Estado General:* {status_text}\n"
        message += f"📅 *Actualizado:* {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        
        if note:
            message += f"ℹ️ *Nota:* {note}\n"
        
        message += "\n"
        
        if services:
            message += "📋 *Servicios:*\n"
            operational_services = 0
            total_services = len(services)
            
            for service in services:
                service_status = service.get('status', 'Unknown')
                service_name = service.get('name', 'Unknown')
                
                if service_status == 'Operational':
                    service_emoji = "🟢"
                    operational_services += 1
                elif service_status == 'Issue':
                    service_emoji = "🔴"
                else:
                    service_emoji = "⚪"
                
                message += f"{service_emoji} *{service_name}*: {service_status}\n"
            
            # Resumen de servicios
            if operational_services == total_services:
                message += f"\n✅ *Todos los servicios operativos* ({operational_services}/{total_services})\n"
            elif operational_services > 0:
                message += f"\n⚠️ *{operational_services}/{total_services} servicios operativos*\n"
            else:
                message += f"\n🚨 *Todos los servicios con problemas* (0/{total_services})\n"
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
            self.application.add_handler(CommandHandler("stats", self.stats_command))
            self.application.add_handler(CommandHandler("status", self.status_command))
            self.application.add_handler(CommandHandler("azure", self.azure_command))
            self.application.add_handler(CommandHandler("gcp", self.gcp_command))
            self.application.add_handler(CommandHandler("aws", self.aws_command))
            self.application.add_handler(CommandHandler("oci", self.oci_command))
            self.application.add_handler(CallbackQueryHandler(self.button_callback))
            
            logger.info("Bot iniciado correctamente")
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)
            
        except Exception as e:
            logger.error(f"Error iniciando el bot: {e}")
            raise

if __name__ == "__main__":
    bot = CloudStatusBot()
    bot.run() 