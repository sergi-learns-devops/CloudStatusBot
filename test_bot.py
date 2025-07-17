#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad del bot
sin necesidad de configurar Telegram
"""

import asyncio
import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cloud_status import CloudStatusChecker
from config import Config
import logging

async def test_cloud_status():
    """Probar la funcionalidad de verificación de estado cloud"""
    print("🧪 Probando funcionalidad del bot de estado cloud...")
    print("=" * 50)
    
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Crear instancia del verificador
    checker = CloudStatusChecker()
    
    try:
        print("\n1️⃣ Probando estado de Azure...")
        azure_status = await checker.get_azure_status()
        print(f"   Resultado: {azure_status.get('overall_status', 'Error')}")
        
        print("\n2️⃣ Probando estado de GCP...")
        gcp_status = await checker.get_gcp_status()
        print(f"   Resultado: {gcp_status.get('overall_status', 'Error')}")
        
        print("\n3️⃣ Probando estado de AWS...")
        aws_status = await checker.get_aws_status()
        print(f"   Resultado: {aws_status.get('overall_status', 'Error')}")
        
        print("\n4️⃣ Probando estado general...")
        all_status = await checker.get_all_status()
        print(f"   Proveedores verificados: {len(all_status)}")
        
        print("\n" + "=" * 50)
        print("✅ Pruebas completadas exitosamente!")
        print("\n📊 Resumen:")
        
        for provider, status in all_status.items():
            if "error" in status:
                print(f"   ❌ {provider.upper()}: Error")
            else:
                overall = status.get('overall_status', 'Unknown')
                emoji = "🟢" if overall == 'Operational' else "🔴"
                print(f"   {emoji} {provider.upper()}: {overall}")
        
        print("\n🎉 ¡El bot está listo para usar!")
        print("   Configura tu token de Telegram y ejecuta 'python main.py'")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        logger.error(f"Error en pruebas: {e}")
        return False
    
    return True

def test_config():
    """Probar la configuración"""
    print("⚙️ Probando configuración...")
    
    try:
        # Intentar cargar configuración
        Config.validate()
        print("   ✅ Configuración válida")
        return True
    except Exception as e:
        print(f"   ❌ Error en configuración: {e}")
        print("   💡 Asegúrate de tener un archivo .env con TELEGRAM_BOT_TOKEN")
        return False

def main():
    """Función principal de pruebas"""
    print("🤖 Bot de Estado de Servicios Cloud - Pruebas")
    print("=" * 50)
    
    # Probar configuración
    if not test_config():
        print("\n❌ Las pruebas fallaron debido a problemas de configuración")
        return
    
    # Probar funcionalidad cloud
    success = asyncio.run(test_cloud_status())
    
    if success:
        print("\n🎯 Próximos pasos:")
        print("1. Crea un bot en Telegram con @BotFather")
        print("2. Copia el token a tu archivo .env")
        print("3. Ejecuta 'python main.py' o 'run.bat' (Windows)")
        print("4. ¡Disfruta monitoreando tus servicios cloud!")
    else:
        print("\n❌ Las pruebas fallaron. Revisa los errores arriba.")

if __name__ == "__main__":
    main() 