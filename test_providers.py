#!/usr/bin/env python3
"""
Script de prueba para diagnosticar problemas con proveedores cloud
"""

import asyncio
import aiohttp
import logging
from cloud_status import CloudStatusChecker
from config import Config

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_provider(provider_name: str, checker: CloudStatusChecker):
    """Probar un proveedor específico"""
    print(f"\n{'='*50}")
    print(f"Probando {provider_name.upper()}")
    print(f"{'='*50}")
    
    try:
        if provider_name == 'azure':
            result = await checker.get_azure_status()
        elif provider_name == 'gcp':
            result = await checker.get_gcp_status()
        elif provider_name == 'aws':
            result = await checker.get_aws_status()
        elif provider_name == 'oci':
            result = await checker.get_oci_status()
        else:
            print(f"Proveedor {provider_name} no soportado")
            return
        
        print(f"Resultado: {result}")
        
        if result.get('error'):
            print(f"❌ Error: {result.get('message')}")
        else:
            print(f"✅ Éxito: {result.get('overall_status')}")
            print(f"📋 Servicios: {len(result.get('services', []))}")
            
    except Exception as e:
        print(f"❌ Excepción: {e}")

async def test_urls():
    """Probar URLs directamente"""
    print(f"\n{'='*50}")
    print("PROBANDO URLs DIRECTAMENTE")
    print(f"{'='*50}")
    
    timeout = aiohttp.ClientTimeout(total=10)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    urls_to_test = [
        ("Azure 1", "https://status.azure.com/en-us/status/"),
        ("Azure 2", "https://azure.microsoft.com/en-us/status/"),
        ("GCP 1", "https://status.cloud.google.com/"),
        ("GCP 2", "https://cloud.google.com/status"),
        ("AWS", "https://status.aws.amazon.com/rss/all.rss"),
        ("OCI 1", "https://ocistatus.oraclecloud.com/"),
        ("OCI 2", "https://status.oraclecloud.com/")
    ]
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for name, url in urls_to_test:
            try:
                print(f"\n🔍 Probando {name}: {url}")
                async with session.get(url, headers=headers) as response:
                    print(f"   Status: {response.status}")
                    if response.status == 200:
                        content = await response.text()
                        print(f"   Tamaño: {len(content)} caracteres")
                        print(f"   Primeros 200 chars: {content[:200]}...")
                        
                        # Buscar indicadores de estado
                        content_lower = content.lower()
                        indicators = []
                        if "operational" in content_lower:
                            indicators.append("operational")
                        if "issue" in content_lower:
                            indicators.append("issue")
                        if "investigating" in content_lower:
                            indicators.append("investigating")
                        if "outage" in content_lower:
                            indicators.append("outage")
                        if "degraded" in content_lower:
                            indicators.append("degraded")
                        
                        print(f"   Indicadores encontrados: {indicators}")
                    else:
                        print(f"   ❌ Error HTTP: {response.status}")
                        
            except Exception as e:
                print(f"   ❌ Error: {e}")

async def main():
    """Función principal"""
    print("🔍 DIAGNÓSTICO DE PROVEEDORES CLOUD")
    print("="*50)
    
    # Probar URLs directamente
    await test_urls()
    
    # Probar con el checker
    print(f"\n{'='*50}")
    print("PROBANDO CON CLOUDSTATUSCHECKER")
    print(f"{'='*50}")
    
    checker = CloudStatusChecker()
    
    providers = ['azure', 'gcp', 'aws', 'oci']
    for provider in providers:
        await test_provider(provider, checker)
    
    # Probar estado general
    print(f"\n{'='*50}")
    print("PROBANDO ESTADO GENERAL")
    print(f"{'='*50}")
    
    try:
        all_status = await checker.get_all_status()
        print(f"Estado general: {all_status}")
    except Exception as e:
        print(f"Error en estado general: {e}")
    
    await checker.close()

if __name__ == "__main__":
    asyncio.run(main()) 