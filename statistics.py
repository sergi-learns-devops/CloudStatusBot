"""
Módulo para manejar estadísticas y métricas del bot
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class BotStatistics:
    """Clase para manejar estadísticas del bot"""
    
    def __init__(self, stats_file: str = "bot_stats.json"):
        self.stats_file = stats_file
        self.stats = self._load_stats()
    
    def _load_stats(self) -> Dict:
        """Cargar estadísticas desde archivo"""
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error cargando estadísticas: {e}")
        
        return {
            'total_commands': 0,
            'commands_by_type': {},
            'uptime_start': datetime.now().isoformat(),
            'last_command': None,
            'daily_stats': {},
            'provider_checks': {
                'azure': {'total': 0, 'success': 0, 'errors': 0},
                'gcp': {'total': 0, 'success': 0, 'errors': 0},
                'aws': {'total': 0, 'success': 0, 'errors': 0},
                'oci': {'total': 0, 'success': 0, 'errors': 0}
            }
        }
    
    def _save_stats(self):
        """Guardar estadísticas en archivo"""
        try:
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error guardando estadísticas: {e}")
    
    def record_command(self, command: str, user_id: Optional[int] = None):
        """Registrar un comando ejecutado"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Incrementar contador total
        self.stats['total_commands'] += 1
        
        # Incrementar contador por tipo de comando
        if command not in self.stats['commands_by_type']:
            self.stats['commands_by_type'][command] = 0
        self.stats['commands_by_type'][command] += 1
        
        # Actualizar último comando
        self.stats['last_command'] = {
            'command': command,
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id
        }
        
        # Estadísticas diarias
        if today not in self.stats['daily_stats']:
            self.stats['daily_stats'][today] = {
                'total_commands': 0,
                'commands_by_type': {}
            }
        
        self.stats['daily_stats'][today]['total_commands'] += 1
        
        if command not in self.stats['daily_stats'][today]['commands_by_type']:
            self.stats['daily_stats'][today]['commands_by_type'][command] = 0
        self.stats['daily_stats'][today]['commands_by_type'][command] += 1
        
        self._save_stats()
    
    def record_provider_check(self, provider: str, success: bool):
        """Registrar verificación de proveedor"""
        if provider in self.stats['provider_checks']:
            self.stats['provider_checks'][provider]['total'] += 1
            if success:
                self.stats['provider_checks'][provider]['success'] += 1
            else:
                self.stats['provider_checks'][provider]['errors'] += 1
        
        self._save_stats()
    
    def get_uptime(self) -> str:
        """Obtener tiempo de actividad del bot"""
        start_time = datetime.fromisoformat(self.stats['uptime_start'])
        uptime = datetime.now() - start_time
        
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m {seconds}s"
    
    def get_stats_summary(self) -> str:
        """Obtener resumen de estadísticas"""
        uptime = self.get_uptime()
        total_commands = self.stats['total_commands']
        
        # Comandos más populares
        popular_commands = sorted(
            self.stats['commands_by_type'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        # Estadísticas de proveedores
        provider_stats = []
        for provider, stats in self.stats['provider_checks'].items():
            if stats['total'] > 0:
                success_rate = (stats['success'] / stats['total']) * 100
                provider_stats.append(f"{provider.upper()}: {success_rate:.1f}%")
        
        summary = f"""
📊 *Estadísticas del Bot*

⏱️ *Tiempo activo:* {uptime}
📈 *Comandos totales:* {total_commands}

🔥 *Comandos más populares:*
"""
        
        for command, count in popular_commands:
            summary += f"• `{command}`: {count} veces\n"
        
        if provider_stats:
            summary += "\n☁️ *Tasa de éxito por proveedor:*\n"
            for stat in provider_stats:
                summary += f"• {stat}\n"
        
        return summary
    
    def get_daily_stats(self, days: int = 7) -> str:
        """Obtener estadísticas de los últimos días"""
        today = datetime.now()
        stats_text = f"📅 *Estadísticas de los últimos {days} días:*\n\n"
        
        for i in range(days):
            date = (today - timedelta(days=i)).strftime('%Y-%m-%d')
            if date in self.stats['daily_stats']:
                daily_data = self.stats['daily_stats'][date]
                stats_text += f"📆 *{date}:*\n"
                stats_text += f"   • Total: {daily_data['total_commands']} comandos\n"
                
                # Comandos más usados del día
                top_commands = sorted(
                    daily_data['commands_by_type'].items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:2]
                
                for command, count in top_commands:
                    stats_text += f"   • `{command}`: {count} veces\n"
                stats_text += "\n"
        
        return stats_text 