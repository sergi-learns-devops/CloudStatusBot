import asyncio
import aiohttp
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging
from config import Config
import re

# Configurar logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL))
logger = logging.getLogger(__name__)

class CloudStatusChecker:
    """Clase para verificar el estado de los servicios cloud"""
    
    def __init__(self):
        self.cache = {}
        self.cache_timestamps = {}
        self.session = None
    
    async def _get_session(self):
        """Obtener sesión HTTP reutilizable"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=Config.HTTP_TIMEOUT)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def _make_request_with_retry(self, url: str, headers: dict = None) -> Optional[str]:
        """Realizar petición HTTP con reintentos"""
        session = await self._get_session()
        headers = headers or Config.HEADERS
        
        for attempt in range(Config.MAX_RETRIES):
            try:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        logger.warning(f"HTTP {response.status} para {url}")
            except asyncio.TimeoutError:
                logger.warning(f"Timeout en intento {attempt + 1} para {url}")
            except Exception as e:
                logger.warning(f"Error en intento {attempt + 1} para {url}: {e}")
            
            if attempt < Config.MAX_RETRIES - 1:
                await asyncio.sleep(1 * (attempt + 1))  # Backoff exponencial
        
        return None
    
    async def get_azure_status(self) -> Dict:
        """Obtener estado de Azure"""
        try:
            # Intentar múltiples fuentes para Azure
            urls = [
                "https://status.azure.com/en-us/status/",
                "https://azure.microsoft.com/en-us/status/"
            ]
            
            for url in urls:
                html_content = await self._make_request_with_retry(url)
                if html_content:
                    return self._parse_azure_html(html_content)
            
            # Si todas las URLs fallan, devolver estado operativo por defecto
            return {
                'provider': 'Azure',
                'overall_status': 'Operational',
                'services': [{'name': 'Azure Services', 'status': 'Operational', 'region': 'Global'}],
                'last_updated': datetime.now().isoformat(),
                'note': 'Estado asumido - no se pudo verificar'
            }
                
        except Exception as e:
            logger.error(f"Error obteniendo estado de Azure: {e}")
            return {"error": True, "message": str(e)}
    
    async def get_gcp_status(self) -> Dict:
        """Obtener estado de Google Cloud Platform"""
        try:
            # Intentar múltiples fuentes para GCP
            urls = [
                "https://status.cloud.google.com/",
                "https://cloud.google.com/status"
            ]
            
            for url in urls:
                html_content = await self._make_request_with_retry(url)
                if html_content:
                    return self._parse_gcp_html(html_content)
            
            # Si todas las URLs fallan, devolver estado operativo por defecto
            return {
                'provider': 'Google Cloud Platform',
                'overall_status': 'Operational',
                'services': [{'name': 'Google Cloud Services', 'status': 'Operational', 'region': 'Global'}],
                'last_updated': datetime.now().isoformat(),
                'note': 'Estado asumido - no se pudo verificar'
            }
                
        except Exception as e:
            logger.error(f"Error obteniendo estado de GCP: {e}")
            return {"error": True, "message": str(e)}
    
    async def get_aws_status(self) -> Dict:
        """Obtener estado de AWS"""
        try:
            # AWS tiene una API RSS que podemos parsear
            url = "https://status.aws.amazon.com/rss/all.rss"
            data = await self._make_request_with_retry(url)
            
            if data:
                return self._parse_aws_data(data)
            else:
                return {"error": True, "message": "No se pudo obtener datos de AWS"}
                
        except Exception as e:
            logger.error(f"Error obteniendo estado de AWS: {e}")
            return {"error": True, "message": str(e)}
    
    async def get_oci_status(self) -> Dict:
        """Obtener estado de Oracle Cloud Infrastructure"""
        try:
            # OCI tiene una página de estado pública
            urls = [
                "https://ocistatus.oraclecloud.com/",
                "https://status.oraclecloud.com/"
            ]
            
            for url in urls:
                html_content = await self._make_request_with_retry(url)
                if html_content:
                    return self._parse_oci_html(html_content)
            
            # Si todas las URLs fallan, devolver estado operativo por defecto
            return {
                'provider': 'Oracle Cloud Infrastructure',
                'overall_status': 'Operational',
                'services': [{'name': 'OCI Services', 'status': 'Operational', 'region': 'Global'}],
                'last_updated': datetime.now().isoformat(),
                'note': 'Estado asumido - no se pudo verificar'
            }
                
        except Exception as e:
            logger.error(f"Error obteniendo estado de OCI: {e}")
            return {"error": True, "message": str(e)}
    
    def _parse_azure_html(self, html_content: str) -> Dict:
        """Parsear HTML de Azure para obtener estado"""
        try:
            # Buscar indicadores de estado en el HTML
            services = []
            
            # Buscar patrones más específicos que indiquen problemas activos
            content_lower = html_content.lower()
            
            # Buscar indicadores de problemas activos (más específicos)
            active_issues = [
                "investigating",
                "service degradation",
                "service disruption",
                "partial outage",
                "major outage",
                "service unavailable"
            ]
            
            # Buscar indicadores de estado operativo
            operational_indicators = [
                "all services are operating normally",
                "no issues reported",
                "all systems operational",
                "service is healthy"
            ]
            
            has_active_issues = any(indicator in content_lower for indicator in active_issues)
            has_operational_indicators = any(indicator in content_lower for indicator in operational_indicators)
            
            if has_active_issues and not has_operational_indicators:
                services.append({
                    'name': 'Azure Services',
                    'status': 'Issue',
                    'region': 'Global'
                })
                overall_status = 'Issues Detected'
            else:
                services.append({
                    'name': 'Azure Services',
                    'status': 'Operational',
                    'region': 'Global'
                })
                overall_status = 'Operational'
            
            return {
                'provider': 'Azure',
                'overall_status': overall_status,
                'services': services,
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error parseando HTML de Azure: {e}")
            return {"error": True, "message": "Error parseando datos"}
    
    def _parse_gcp_html(self, html_content: str) -> Dict:
        """Parsear HTML de GCP para obtener estado"""
        try:
            services = []
            
            # Buscar patrones más específicos que indiquen problemas activos
            content_lower = html_content.lower()
            
            # Buscar indicadores de problemas activos (más específicos)
            active_issues = [
                "investigating",
                "service degradation",
                "service disruption",
                "partial outage",
                "major outage",
                "service unavailable",
                "ongoing issue"
            ]
            
            # Buscar indicadores de estado operativo
            operational_indicators = [
                "all services are operating normally",
                "no issues reported",
                "all systems operational",
                "service is healthy",
                "operational"
            ]
            
            has_active_issues = any(indicator in content_lower for indicator in active_issues)
            has_operational_indicators = any(indicator in content_lower for indicator in operational_indicators)
            
            if has_active_issues and not has_operational_indicators:
                services.append({
                    'name': 'Google Cloud Services',
                    'status': 'Issue',
                    'region': 'Global'
                })
                overall_status = 'Issues Detected'
            else:
                services.append({
                    'name': 'Google Cloud Services',
                    'status': 'Operational',
                    'region': 'Global'
                })
                overall_status = 'Operational'
            
            return {
                'provider': 'Google Cloud Platform',
                'overall_status': overall_status,
                'services': services,
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error parseando HTML de GCP: {e}")
            return {"error": True, "message": "Error parseando datos"}
    
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
            return {"error": True, "message": "Error parseando datos"}
    
    def _parse_oci_html(self, html_content: str) -> Dict:
        """Parsear HTML de OCI para obtener estado"""
        try:
            services = []
            
            # Buscar patrones que indiquen problemas en OCI
            if "investigating" in html_content.lower() or "issue" in html_content.lower() or "outage" in html_content.lower() or "degraded" in html_content.lower():
                services.append({
                    'name': 'OCI Services',
                    'status': 'Issue',
                    'region': 'Global'
                })
                overall_status = 'Issues Detected'
            else:
                services.append({
                    'name': 'OCI Services',
                    'status': 'Operational',
                    'region': 'Global'
                })
                overall_status = 'Operational'
            
            return {
                'provider': 'Oracle Cloud Infrastructure',
                'overall_status': overall_status,
                'services': services,
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error parseando HTML de OCI: {e}")
            return {"error": True, "message": "Error parseando datos"}
    
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
            'aws': self.get_aws_status,
            'oci': self.get_oci_status
        }
        
        # Ejecutar todas las verificaciones en paralelo para mejor rendimiento
        tasks = []
        for provider_name, provider_func in providers.items():
            if self._is_cache_valid(provider_name):
                results[provider_name] = self.cache[provider_name]
                logger.info(f"Usando caché para {provider_name}")
            else:
                logger.info(f"Obteniendo estado actual de {provider_name}")
                tasks.append((provider_name, provider_func()))
        
        # Ejecutar tareas en paralelo
        if tasks:
            task_results = await asyncio.gather(*[task for _, task in tasks], return_exceptions=True)
            
            for i, (provider_name, _) in enumerate(tasks):
                if isinstance(task_results[i], Exception):
                    logger.error(f"Error obteniendo estado de {provider_name}: {task_results[i]}")
                    results[provider_name] = {"error": True, "message": str(task_results[i])}
                else:
                    results[provider_name] = task_results[i]
                    self.cache[provider_name] = task_results[i]
                    self.cache_timestamps[provider_name] = datetime.now()
        
        return results
    
    async def get_provider_status(self, provider: str) -> Dict:
        """Obtener estado de un proveedor específico"""
        provider = provider.lower()
        
        provider_functions = {
            'azure': self.get_azure_status,
            'gcp': self.get_gcp_status,
            'aws': self.get_aws_status,
            'oci': self.get_oci_status
        }
        
        if provider in provider_functions:
            if self._is_cache_valid(provider):
                return self.cache[provider]
            status = await provider_functions[provider]()
            self.cache[provider] = status
            self.cache_timestamps[provider] = datetime.now()
            return status
        else:
            return {"error": True, "message": f"Proveedor '{provider}' no soportado"}
    
    async def close(self):
        """Cerrar sesión HTTP"""
        if self.session and not self.session.closed:
            await self.session.close() 