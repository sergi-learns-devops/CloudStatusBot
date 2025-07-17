import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from config import Config

# Configurar logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class CloudStatusChecker:
    """Clase para verificar el estado de los servicios cloud"""
    
    def __init__(self):
        self.cache = {}
        self.cache_timestamps = {}
    
    async def get_azure_status(self) -> Dict:
        """Obtener estado de Azure"""
        try:
            async with aiohttp.ClientSession() as session:
                # Azure tiene una API JSON específica
                url = "https://azure.microsoft.com/api/status"
                async with session.get(url, headers=Config.HEADERS) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_azure_data(data)
                    else:
                        return {"status": "error", "message": f"Error HTTP {response.status}"}
        except Exception as e:
            logger.error(f"Error obteniendo estado de Azure: {e}")
            return {"status": "error", "message": str(e)}
    
    async def get_gcp_status(self) -> Dict:
        """Obtener estado de Google Cloud Platform"""
        try:
            async with aiohttp.ClientSession() as session:
                # GCP tiene una API específica para el estado
                url = "https://status.cloud.google.com/incidents.json"
                async with session.get(url, headers=Config.HEADERS) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_gcp_data(data)
                    else:
                        return {"status": "error", "message": f"Error HTTP {response.status}"}
        except Exception as e:
            logger.error(f"Error obteniendo estado de GCP: {e}")
            return {"status": "error", "message": str(e)}
    
    async def get_aws_status(self) -> Dict:
        """Obtener estado de AWS"""
        try:
            async with aiohttp.ClientSession() as session:
                # AWS tiene una API RSS que podemos parsear
                url = "https://status.aws.amazon.com/rss/all.rss"
                async with session.get(url, headers=Config.HEADERS) as response:
                    if response.status == 200:
                        data = await response.text()
                        return self._parse_aws_data(data)
                    else:
                        return {"status": "error", "message": f"Error HTTP {response.status}"}
        except Exception as e:
            logger.error(f"Error obteniendo estado de AWS: {e}")
            return {"status": "error", "message": str(e)}
    
    def _parse_azure_data(self, data: Dict) -> Dict:
        """Parsear datos de Azure"""
        try:
            services = []
            for service in data.get('services', []):
                services.append({
                    'name': service.get('name', 'Unknown'),
                    'status': service.get('status', 'Unknown'),
                    'region': service.get('region', 'Global')
                })
            
            return {
                'provider': 'Azure',
                'overall_status': 'Operational' if all(s['status'] == 'Operational' for s in services) else 'Issues Detected',
                'services': services,
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error parseando datos de Azure: {e}")
            return {"status": "error", "message": "Error parseando datos"}
    
    def _parse_gcp_data(self, data: Dict) -> Dict:
        """Parsear datos de GCP"""
        try:
            services = []
            for incident in data.get('incidents', []):
                services.append({
                    'name': incident.get('service_name', 'Unknown'),
                    'status': 'Issue' if incident.get('status') != 'resolved' else 'Operational',
                    'description': incident.get('title', 'No description'),
                    'region': incident.get('affected_locations', ['Global'])[0] if incident.get('affected_locations') else 'Global'
                })
            
            # Si no hay incidentes, asumimos que todo está operativo
            if not services:
                services = [{'name': 'All Services', 'status': 'Operational', 'region': 'Global'}]
            
            return {
                'provider': 'Google Cloud Platform',
                'overall_status': 'Operational' if all(s['status'] == 'Operational' for s in services) else 'Issues Detected',
                'services': services,
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error parseando datos de GCP: {e}")
            return {"status": "error", "message": "Error parseando datos"}
    
    def _parse_aws_data(self, data: str) -> Dict:
        """Parsear datos de AWS desde RSS"""
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(data)
            
            services = []
            for item in root.findall('.//item'):
                title = item.find('title').text if item.find('title') is not None else 'Unknown'
                description = item.find('description').text if item.find('description') is not None else 'No description'
                
                # Determinar si es un problema activo
                status = 'Issue' if 'investigating' in description.lower() or 'issue' in description.lower() else 'Operational'
                
                services.append({
                    'name': title,
                    'status': status,
                    'description': description,
                    'region': 'Global'
                })
            
            # Si no hay items, asumimos que todo está operativo
            if not services:
                services = [{'name': 'All Services', 'status': 'Operational', 'region': 'Global'}]
            
            return {
                'provider': 'AWS',
                'overall_status': 'Operational' if all(s['status'] == 'Operational' for s in services) else 'Issues Detected',
                'services': services,
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error parseando datos de AWS: {e}")
            return {"status": "error", "message": "Error parseando datos"}
    
    def _is_cache_valid(self, provider: str) -> bool:
        """Verificar si el caché es válido para un proveedor"""
        if provider not in self.cache_timestamps:
            return False
        
        cache_time = self.cache_timestamps[provider]
        return datetime.now() - cache_time < timedelta(seconds=Config.CACHE_DURATION)
    
    async def get_all_status(self) -> Dict:
        """Obtener estado de todos los proveedores cloud"""
        results = {}
        
        # Verificar caché para cada proveedor
        providers = {
            'azure': self.get_azure_status,
            'gcp': self.get_gcp_status,
            'aws': self.get_aws_status
        }
        
        for provider_name, provider_func in providers.items():
            if self._is_cache_valid(provider_name):
                results[provider_name] = self.cache[provider_name]
                logger.info(f"Usando caché para {provider_name}")
            else:
                logger.info(f"Obteniendo estado actual de {provider_name}")
                status = await provider_func()
                self.cache[provider_name] = status
                self.cache_timestamps[provider_name] = datetime.now()
                results[provider_name] = status
        
        return results
    
    async def get_provider_status(self, provider: str) -> Dict:
        """Obtener estado de un proveedor específico"""
        provider = provider.lower()
        
        if provider == 'azure':
            if self._is_cache_valid('azure'):
                return self.cache['azure']
            status = await self.get_azure_status()
            self.cache['azure'] = status
            self.cache_timestamps['azure'] = datetime.now()
            return status
        elif provider == 'gcp':
            if self._is_cache_valid('gcp'):
                return self.cache['gcp']
            status = await self.get_gcp_status()
            self.cache['gcp'] = status
            self.cache_timestamps['gcp'] = datetime.now()
            return status
        elif provider == 'aws':
            if self._is_cache_valid('aws'):
                return self.cache['aws']
            status = await self.get_aws_status()
            self.cache['aws'] = status
            self.cache_timestamps['aws'] = datetime.now()
            return status
        else:
            return {"status": "error", "message": f"Proveedor '{provider}' no soportado"} 