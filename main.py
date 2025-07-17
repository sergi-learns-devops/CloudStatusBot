#!/usr/bin/env python3
"""
Bot de Telegram para monitorear el estado de servicios cloud
Soporta Azure, Google Cloud Platform y AWS
"""

import sys
import os

# Agregar el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from telegram_bot import CloudStatusBot
from config import Config
import logging

def main():
    """Función principal para ejecutar el bot"""
    try:
        # Configurar logging
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        logger = logging.getLogger(__name__)
        
        logger.info("Iniciando Bot de Estado de Servicios Cloud...")
        
        # Validar configuración
        Config.validate()
        logger.info("Configuración validada correctamente")
        
        # Crear y ejecutar el bot
        bot = CloudStatusBot()
        logger.info("Bot creado, iniciando...")
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"Error fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 