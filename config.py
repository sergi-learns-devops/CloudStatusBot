import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración del bot de Telegram para monitoreo de servicios cloud"""
    
    # Token del bot de Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Duración del caché en segundos (5 minutos por defecto)
    CACHE_DURATION = int(os.getenv('CACHE_DURATION', 300))
    
    # Timeout para peticiones HTTP (10 segundos por defecto)
    HTTP_TIMEOUT = int(os.getenv('HTTP_TIMEOUT', 10))
    
    # Número máximo de reintentos para peticiones HTTP
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    
    # URLs de las APIs de estado
    AZURE_STATUS_URL = os.getenv('AZURE_STATUS_URL', 'https://status.azure.com/en-us/status/')
    GCP_STATUS_URL = os.getenv('GCP_STATUS_URL', 'https://status.cloud.google.com/')
    AWS_STATUS_URL = os.getenv('AWS_STATUS_URL', 'https://status.aws.amazon.com/')
    
    # Nivel de logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Configuración de estadísticas
    ENABLE_STATISTICS = os.getenv('ENABLE_STATISTICS', 'true').lower() == 'true'
    
    # Headers para las peticiones HTTP
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    @classmethod
    def validate(cls):
        """Validar que las configuraciones requeridas estén presentes"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN es requerido en las variables de entorno")
        return True 