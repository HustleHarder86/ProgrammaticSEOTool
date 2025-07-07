#!/usr/bin/env python3
"""
System Health Monitoring Script for Programmatic SEO Tool
Monitors API endpoints, database connectivity, and performance metrics
"""

import requests
import json
import time
import psutil
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
import sqlite3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitoring.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


class HealthMonitor:
    def __init__(self, backend_url: str, frontend_url: str = None):
        self.backend_url = backend_url.rstrip('/')
        self.frontend_url = frontend_url.rstrip('/') if frontend_url else None
        self.metrics = {
            'checks_performed': 0,
            'uptime_percentage': 100.0,
            'avg_response_time': 0.0,
            'failures': [],
            'warnings': []
        }
        self.check_history = []
        
    def check_backend_health(self) -> Dict[str, Any]:
        """Check backend API health"""
        result = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'backend',
            'checks': {}
        }
        
        # Health endpoint check
        try:
            start_time = time.time()
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                result['checks']['health'] = {
                    'status': 'healthy',
                    'response_time_ms': round(response_time, 2),
                    'database': data.get('database', 'unknown')
                }
            else:
                result['checks']['health'] = {
                    'status': 'unhealthy',
                    'error': f'HTTP {response.status_code}',
                    'response_time_ms': round(response_time, 2)
                }
        except Exception as e:
            result['checks']['health'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # API test endpoint check
        try:
            start_time = time.time()
            response = requests.get(f"{self.backend_url}/api/test", timeout=5)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result['checks']['api_test'] = {
                    'status': 'healthy',
                    'response_time_ms': round(response_time, 2)
                }
            else:
                result['checks']['api_test'] = {
                    'status': 'unhealthy',
                    'error': f'HTTP {response.status_code}'
                }
        except Exception as e:
            result['checks']['api_test'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Calculate overall status
        all_checks = list(result['checks'].values())
        if all(check.get('status') == 'healthy' for check in all_checks):
            result['overall_status'] = 'healthy'
        elif any(check.get('status') == 'error' for check in all_checks):
            result['overall_status'] = 'error'
        else:
            result['overall_status'] = 'degraded'
        
        return result
    
    def check_frontend_health(self) -> Optional[Dict[str, Any]]:
        """Check frontend health if URL provided"""
        if not self.frontend_url:
            return None
            
        result = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'frontend',
            'checks': {}
        }
        
        try:
            start_time = time.time()
            response = requests.get(self.frontend_url, timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                result['checks']['homepage'] = {
                    'status': 'healthy',
                    'response_time_ms': round(response_time, 2),
                    'content_length': len(response.content)
                }
                result['overall_status'] = 'healthy'
            else:
                result['checks']['homepage'] = {
                    'status': 'unhealthy',
                    'error': f'HTTP {response.status_code}',
                    'response_time_ms': round(response_time, 2)
                }
                result['overall_status'] = 'unhealthy'
        except Exception as e:
            result['checks']['homepage'] = {
                'status': 'error',
                'error': str(e)
            }
            result['overall_status'] = 'error'
        
        return result
    
    def check_system_resources(self) -> Dict[str, Any]:
        """Check system resource usage"""
        result = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'system',
            'metrics': {}
        }
        
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            result['metrics']['cpu'] = {
                'usage_percent': cpu_percent,
                'status': 'healthy' if cpu_percent < 80 else 'warning' if cpu_percent < 90 else 'critical'
            }
            
            # Memory usage
            memory = psutil.virtual_memory()
            result['metrics']['memory'] = {
                'usage_percent': memory.percent,
                'available_mb': round(memory.available / 1024 / 1024, 2),
                'status': 'healthy' if memory.percent < 80 else 'warning' if memory.percent < 90 else 'critical'
            }
            
            # Disk usage
            disk = psutil.disk_usage('/')
            result['metrics']['disk'] = {
                'usage_percent': disk.percent,
                'free_gb': round(disk.free / 1024 / 1024 / 1024, 2),
                'status': 'healthy' if disk.percent < 80 else 'warning' if disk.percent < 90 else 'critical'
            }
            
            result['overall_status'] = 'healthy'
            for metric in result['metrics'].values():
                if metric['status'] == 'critical':
                    result['overall_status'] = 'critical'
                    break
                elif metric['status'] == 'warning' and result['overall_status'] != 'critical':
                    result['overall_status'] = 'warning'
                    
        except Exception as e:
            result['overall_status'] = 'error'
            result['error'] = str(e)
        
        return result
    
    def check_database_health(self) -> Dict[str, Any]:
        """Check database health and statistics"""
        result = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': 'database',
            'checks': {}
        }
        
        db_path = os.path.join(os.path.dirname(__file__), 'programmatic_seo.db')
        
        try:
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Check database size
                db_size = os.path.getsize(db_path)
                result['checks']['size'] = {
                    'size_mb': round(db_size / 1024 / 1024, 2),
                    'status': 'healthy' if db_size < 100 * 1024 * 1024 else 'warning'  # Warning if > 100MB
                }
                
                # Count records in main tables
                tables = ['projects', 'templates', 'data_sets', 'generated_pages']
                for table in tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        result['checks'][f'{table}_count'] = count
                    except:
                        result['checks'][f'{table}_count'] = 'error'
                
                conn.close()
                result['overall_status'] = 'healthy'
            else:
                result['checks']['database'] = 'not_found'
                result['overall_status'] = 'error'
                
        except Exception as e:
            result['overall_status'] = 'error'
            result['error'] = str(e)
        
        return result
    
    def perform_full_check(self) -> Dict[str, Any]:
        """Perform all health checks"""
        logger.info("Performing full system health check...")
        
        full_result = {
            'timestamp': datetime.utcnow().isoformat(),
            'checks': {}
        }
        
        # Backend health
        backend_result = self.check_backend_health()
        full_result['checks']['backend'] = backend_result
        
        # Frontend health (if configured)
        if self.frontend_url:
            frontend_result = self.check_frontend_health()
            full_result['checks']['frontend'] = frontend_result
        
        # System resources
        system_result = self.check_system_resources()
        full_result['checks']['system'] = system_result
        
        # Database health
        db_result = self.check_database_health()
        full_result['checks']['database'] = db_result
        
        # Calculate overall status
        all_statuses = [check.get('overall_status', 'unknown') 
                       for check in full_result['checks'].values()]
        
        if all(status == 'healthy' for status in all_statuses):
            full_result['overall_status'] = 'healthy'
        elif any(status == 'error' for status in all_statuses):
            full_result['overall_status'] = 'error'
        elif any(status == 'critical' for status in all_statuses):
            full_result['overall_status'] = 'critical'
        elif any(status == 'warning' for status in all_statuses):
            full_result['overall_status'] = 'warning'
        else:
            full_result['overall_status'] = 'degraded'
        
        # Update metrics
        self.metrics['checks_performed'] += 1
        self.check_history.append(full_result)
        
        # Keep only last 100 checks
        if len(self.check_history) > 100:
            self.check_history = self.check_history[-100:]
        
        # Calculate uptime percentage
        healthy_checks = sum(1 for check in self.check_history 
                           if check['overall_status'] == 'healthy')
        self.metrics['uptime_percentage'] = (healthy_checks / len(self.check_history)) * 100
        
        # Log result
        logger.info(f"Health check complete: {full_result['overall_status']}")
        
        return full_result
    
    def generate_report(self) -> str:
        """Generate a health report"""
        report = []
        report.append("="*60)
        report.append("PROGRAMMATIC SEO TOOL - HEALTH REPORT")
        report.append("="*60)
        report.append(f"Generated: {datetime.utcnow().isoformat()}")
        report.append(f"Backend URL: {self.backend_url}")
        if self.frontend_url:
            report.append(f"Frontend URL: {self.frontend_url}")
        report.append("")
        
        # Latest check result
        if self.check_history:
            latest = self.check_history[-1]
            report.append(f"Latest Status: {latest['overall_status'].upper()}")
            report.append("")
            
            # Service statuses
            report.append("Service Status:")
            for service, check in latest['checks'].items():
                status = check.get('overall_status', 'unknown')
                report.append(f"  - {service.capitalize()}: {status}")
            report.append("")
        
        # Metrics
        report.append("Metrics:")
        report.append(f"  - Checks Performed: {self.metrics['checks_performed']}")
        report.append(f"  - Uptime: {self.metrics['uptime_percentage']:.1f}%")
        report.append("")
        
        # Recent issues
        if self.metrics['failures']:
            report.append("Recent Failures:")
            for failure in self.metrics['failures'][-5:]:
                report.append(f"  - {failure}")
            report.append("")
        
        if self.metrics['warnings']:
            report.append("Recent Warnings:")
            for warning in self.metrics['warnings'][-5:]:
                report.append(f"  - {warning}")
            report.append("")
        
        report.append("="*60)
        
        return "\n".join(report)
    
    def continuous_monitoring(self, interval_seconds: int = 60):
        """Run continuous monitoring"""
        logger.info(f"Starting continuous monitoring (interval: {interval_seconds}s)")
        
        try:
            while True:
                result = self.perform_full_check()
                
                # Check for issues and log them
                if result['overall_status'] in ['error', 'critical']:
                    error_msg = f"{datetime.utcnow().isoformat()} - System {result['overall_status']}"
                    self.metrics['failures'].append(error_msg)
                    logger.error(error_msg)
                elif result['overall_status'] == 'warning':
                    warning_msg = f"{datetime.utcnow().isoformat()} - System warning"
                    self.metrics['warnings'].append(warning_msg)
                    logger.warning(warning_msg)
                
                # Print summary every 10 checks
                if self.metrics['checks_performed'] % 10 == 0:
                    print("\n" + self.generate_report())
                
                # Sleep until next check
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
            print("\n" + self.generate_report())
        except Exception as e:
            logger.error(f"Monitoring error: {str(e)}")
            raise


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor Programmatic SEO Tool health')
    parser.add_argument('--backend-url', 
                       default='https://programmaticseotool-production.up.railway.app',
                       help='Backend API URL')
    parser.add_argument('--frontend-url',
                       default='https://programmatic-seo-tool.vercel.app',
                       help='Frontend URL (optional)')
    parser.add_argument('--interval', 
                       type=int, 
                       default=60,
                       help='Check interval in seconds')
    parser.add_argument('--once', 
                       action='store_true',
                       help='Run once and exit')
    
    args = parser.parse_args()
    
    monitor = HealthMonitor(args.backend_url, args.frontend_url)
    
    if args.once:
        result = monitor.perform_full_check()
        print(json.dumps(result, indent=2))
        print("\n" + monitor.generate_report())
    else:
        monitor.continuous_monitoring(args.interval)


if __name__ == "__main__":
    main()