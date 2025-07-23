"""Scheduler for automated content generation and publishing"""

import schedule
import time
import threading
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


class ContentScheduler:
    """Manages scheduled content generation and publishing tasks"""
    
    def __init__(self, config_file: str = "scheduler_config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.jobs = {}
        self.job_history = defaultdict(list)
        self.running = False
        self.thread = None
        
    def _load_config(self) -> Dict[str, Any]:
        """Load scheduler configuration"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading scheduler config: {e}")
                return self._default_config()
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """Default scheduler configuration"""
        return {
            "timezone": "UTC",
            "max_concurrent_jobs": 3,
            "job_timeout": 3600,  # 1 hour
            "retry_failed": True,
            "retry_count": 3,
            "notification_email": "",
            "log_retention_days": 30
        }
    
    def _save_config(self):
        """Save current configuration"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving scheduler config: {e}")
    
    def add_job(self,
               job_id: str,
               job_type: str,
               schedule_pattern: str,
               job_config: Dict[str, Any],
               callback: Callable):
        """Add a scheduled job
        
        Args:
            job_id: Unique job identifier
            job_type: Type of job (generate, publish, etc.)
            schedule_pattern: Schedule pattern (daily, weekly, cron)
            job_config: Job-specific configuration
            callback: Function to call when job runs
        """
        job_data = {
            "id": job_id,
            "type": job_type,
            "schedule": schedule_pattern,
            "config": job_config,
            "callback": callback,
            "created": datetime.now().isoformat(),
            "enabled": True,
            "last_run": None,
            "next_run": None
        }
        
        # Parse schedule and set up job
        self._schedule_job(job_data)
        
        # Store job
        self.jobs[job_id] = job_data
        
        logger.info(f"Added scheduled job: {job_id} ({job_type}) - {schedule_pattern}")
    
    def _schedule_job(self, job_data: Dict[str, Any]):
        """Set up scheduled job based on pattern"""
        pattern = job_data["schedule"]
        job_func = lambda: self._run_job(job_data)
        
        # Daily patterns
        if pattern.startswith("daily"):
            if "@" in pattern:
                # daily@10:30
                time_str = pattern.split("@")[1]
                schedule.every().day.at(time_str).do(job_func)
            else:
                # daily
                schedule.every().day.do(job_func)
        
        # Weekly patterns
        elif pattern.startswith("weekly"):
            if "@" in pattern:
                # weekly:monday@10:30
                parts = pattern.split(":")
                day = parts[1].split("@")[0]
                time_str = parts[1].split("@")[1]
                getattr(schedule.every(), day.lower()).at(time_str).do(job_func)
            else:
                # weekly
                schedule.every().week.do(job_func)
        
        # Hourly patterns
        elif pattern.startswith("hourly"):
            if ":" in pattern:
                # hourly:30 (every hour at 30 minutes)
                minutes = pattern.split(":")[1]
                schedule.every().hour.at(f":{minutes}").do(job_func)
            else:
                # hourly
                schedule.every().hour.do(job_func)
        
        # Every X minutes/hours
        elif pattern.startswith("every"):
            parts = pattern.split(" ")
            if len(parts) >= 3:
                amount = int(parts[1])
                unit = parts[2]
                
                if unit == "minutes":
                    schedule.every(amount).minutes.do(job_func)
                elif unit == "hours":
                    schedule.every(amount).hours.do(job_func)
                elif unit == "days":
                    schedule.every(amount).days.do(job_func)
        
        # Custom cron-like patterns
        elif pattern.startswith("cron:"):
            # cron:0 0 * * * (midnight daily)
            # This would require a cron parser - simplified for now
            logger.warning(f"Cron patterns not fully implemented: {pattern}")
            schedule.every().day.do(job_func)
        
        # Update next run time
        job_data["next_run"] = self._get_next_run_time(pattern)
    
    def _run_job(self, job_data: Dict[str, Any]):
        """Execute a scheduled job"""
        job_id = job_data["id"]
        
        if not job_data["enabled"]:
            logger.info(f"Job {job_id} is disabled, skipping")
            return
        
        logger.info(f"Running scheduled job: {job_id}")
        
        # Record start
        run_record = {
            "job_id": job_id,
            "start_time": datetime.now().isoformat(),
            "status": "running"
        }
        
        try:
            # Execute callback
            callback = job_data["callback"]
            result = callback(job_data["config"])
            
            # Record success
            run_record["end_time"] = datetime.now().isoformat()
            run_record["status"] = "success"
            run_record["result"] = result
            
            logger.info(f"Job {job_id} completed successfully")
            
        except Exception as e:
            # Record failure
            run_record["end_time"] = datetime.now().isoformat()
            run_record["status"] = "failed"
            run_record["error"] = str(e)
            
            logger.error(f"Job {job_id} failed: {str(e)}")
            
            # Retry if configured
            if self.config.get("retry_failed", True):
                self._schedule_retry(job_data, run_record)
        
        # Update job data
        job_data["last_run"] = run_record["end_time"]
        job_data["next_run"] = self._get_next_run_time(job_data["schedule"])
        
        # Store history
        self.job_history[job_id].append(run_record)
        self._cleanup_old_history()
    
    def _schedule_retry(self, job_data: Dict[str, Any], run_record: Dict[str, Any]):
        """Schedule a retry for failed job"""
        retry_count = run_record.get("retry_count", 0)
        max_retries = self.config.get("retry_count", 3)
        
        if retry_count < max_retries:
            # Schedule retry in 5 minutes
            retry_job = job_data.copy()
            retry_job["id"] = f"{job_data['id']}_retry_{retry_count + 1}"
            run_record["retry_count"] = retry_count + 1
            
            schedule.every(5).minutes.do(lambda: self._run_job(retry_job)).tag("retry")
            logger.info(f"Scheduled retry {retry_count + 1} for job {job_data['id']}")
    
    def _get_next_run_time(self, pattern: str) -> Optional[str]:
        """Calculate next run time based on pattern"""
        # Simplified - would need proper implementation
        now = datetime.now()
        
        if pattern.startswith("daily"):
            next_run = now + timedelta(days=1)
        elif pattern.startswith("hourly"):
            next_run = now + timedelta(hours=1)
        elif pattern.startswith("weekly"):
            next_run = now + timedelta(weeks=1)
        else:
            next_run = now + timedelta(hours=1)
        
        return next_run.isoformat()
    
    def _cleanup_old_history(self):
        """Remove old job history records"""
        retention_days = self.config.get("log_retention_days", 30)
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        for job_id in self.job_history:
            self.job_history[job_id] = [
                record for record in self.job_history[job_id]
                if datetime.fromisoformat(record["start_time"]) > cutoff_date
            ]
    
    def start(self):
        """Start the scheduler"""
        if self.running:
            logger.warning("Scheduler already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        logger.info("Scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Scheduler stopped")
    
    def _run_scheduler(self):
        """Main scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def remove_job(self, job_id: str):
        """Remove a scheduled job"""
        if job_id in self.jobs:
            # Cancel scheduled job
            schedule.clear(job_id)
            del self.jobs[job_id]
            logger.info(f"Removed job: {job_id}")
    
    def enable_job(self, job_id: str):
        """Enable a job"""
        if job_id in self.jobs:
            self.jobs[job_id]["enabled"] = True
            logger.info(f"Enabled job: {job_id}")
    
    def disable_job(self, job_id: str):
        """Disable a job"""
        if job_id in self.jobs:
            self.jobs[job_id]["enabled"] = False
            logger.info(f"Disabled job: {job_id}")
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get job status and history"""
        if job_id not in self.jobs:
            return {"error": "Job not found"}
        
        job = self.jobs[job_id]
        history = self.job_history.get(job_id, [])
        
        # Calculate stats
        total_runs = len(history)
        successful_runs = sum(1 for h in history if h["status"] == "success")
        failed_runs = sum(1 for h in history if h["status"] == "failed")
        
        return {
            "job": job,
            "stats": {
                "total_runs": total_runs,
                "successful": successful_runs,
                "failed": failed_runs,
                "success_rate": successful_runs / total_runs if total_runs > 0 else 0
            },
            "recent_history": history[-10:]  # Last 10 runs
        }
    
    def list_jobs(self) -> List[Dict[str, Any]]:
        """List all scheduled jobs"""
        return [
            {
                "id": job_id,
                "type": job["type"],
                "schedule": job["schedule"],
                "enabled": job["enabled"],
                "last_run": job["last_run"],
                "next_run": job["next_run"]
            }
            for job_id, job in self.jobs.items()
        ]
    
    def export_config(self) -> Dict[str, Any]:
        """Export scheduler configuration and jobs"""
        return {
            "config": self.config,
            "jobs": [
                {
                    "id": job_id,
                    "type": job["type"],
                    "schedule": job["schedule"],
                    "config": job["config"],
                    "enabled": job["enabled"]
                }
                for job_id, job in self.jobs.items()
            ]
        }
    
    def import_config(self, config_data: Dict[str, Any]):
        """Import scheduler configuration and jobs"""
        if "config" in config_data:
            self.config.update(config_data["config"])
            self._save_config()
        
        if "jobs" in config_data:
            # Note: Callbacks need to be re-registered after import
            logger.warning("Imported jobs need callbacks to be re-registered")


# Singleton instance
_scheduler = None


def get_scheduler() -> ContentScheduler:
    """Get or create singleton scheduler instance"""
    global _scheduler
    if _scheduler is None:
        _scheduler = ContentScheduler()
    return _scheduler