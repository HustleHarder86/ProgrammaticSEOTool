"""Automation Engine for programmatic SEO workflows"""

import json
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
import asyncio
from pathlib import Path
import logging
from dataclasses import dataclass
from enum import Enum

from scheduler import get_scheduler
from smart_page_generator import SmartPageGenerator
from publishers.wordpress_publisher import WordPressPublisher
from publishers.webflow_publisher import WebflowPublisher
from schema_generator import SchemaGenerator

logger = logging.getLogger(__name__)


class WorkflowStatus(Enum):
    """Workflow execution status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


@dataclass
class WorkflowStep:
    """Single step in an automation workflow"""
    name: str
    action: str
    config: Dict[str, Any]
    depends_on: List[str] = None
    retry_on_failure: bool = True
    max_retries: int = 3


class AutomationEngine:
    """Orchestrates automated content generation and publishing workflows"""
    
    def __init__(self):
        self.scheduler = get_scheduler()
        self.page_generator = SmartPageGenerator()
        self.schema_generator = SchemaGenerator()
        self.publishers = {}
        self.workflows = {}
        self.workflow_history = {}
        self._load_workflows()
    
    def _load_workflows(self):
        """Load saved workflows from configuration"""
        workflow_file = Path("automation_workflows.json")
        if workflow_file.exists():
            try:
                with open(workflow_file, 'r') as f:
                    data = json.load(f)
                    self.workflows = data.get("workflows", {})
            except Exception as e:
                logger.error(f"Error loading workflows: {e}")
    
    def create_workflow(self,
                       workflow_id: str,
                       name: str,
                       description: str,
                       steps: List[WorkflowStep],
                       schedule: Optional[str] = None) -> Dict[str, Any]:
        """Create a new automation workflow
        
        Args:
            workflow_id: Unique workflow identifier
            name: Workflow name
            description: Workflow description
            steps: List of workflow steps
            schedule: Optional schedule pattern
            
        Returns:
            Workflow configuration
        """
        workflow = {
            "id": workflow_id,
            "name": name,
            "description": description,
            "steps": [self._step_to_dict(step) for step in steps],
            "schedule": schedule,
            "created": datetime.now().isoformat(),
            "enabled": True,
            "last_run": None,
            "run_count": 0
        }
        
        self.workflows[workflow_id] = workflow
        
        # Schedule if pattern provided
        if schedule:
            self.scheduler.add_job(
                job_id=f"workflow_{workflow_id}",
                job_type="workflow",
                schedule_pattern=schedule,
                job_config={"workflow_id": workflow_id},
                callback=self.execute_workflow
            )
        
        self._save_workflows()
        logger.info(f"Created workflow: {workflow_id} - {name}")
        
        return workflow
    
    def _step_to_dict(self, step: WorkflowStep) -> Dict[str, Any]:
        """Convert WorkflowStep to dictionary"""
        return {
            "name": step.name,
            "action": step.action,
            "config": step.config,
            "depends_on": step.depends_on or [],
            "retry_on_failure": step.retry_on_failure,
            "max_retries": step.max_retries
        }
    
    def _save_workflows(self):
        """Save workflows to configuration file"""
        try:
            with open("automation_workflows.json", 'w') as f:
                json.dump({"workflows": self.workflows}, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving workflows: {e}")
    
    async def execute_workflow(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an automation workflow
        
        Args:
            config: Workflow configuration or {"workflow_id": "..."}
            
        Returns:
            Execution results
        """
        workflow_id = config.get("workflow_id")
        if not workflow_id or workflow_id not in self.workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.workflows[workflow_id]
        
        # Create execution record
        execution_id = f"{workflow_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        execution = {
            "id": execution_id,
            "workflow_id": workflow_id,
            "status": WorkflowStatus.RUNNING.value,
            "start_time": datetime.now().isoformat(),
            "steps_completed": [],
            "steps_failed": [],
            "results": {}
        }
        
        logger.info(f"Starting workflow execution: {execution_id}")
        
        try:
            # Execute steps
            for step_config in workflow["steps"]:
                step_result = await self._execute_step(
                    step_config, 
                    execution["results"]
                )
                
                if step_result["success"]:
                    execution["steps_completed"].append(step_config["name"])
                    execution["results"][step_config["name"]] = step_result["data"]
                else:
                    execution["steps_failed"].append(step_config["name"])
                    execution["results"][step_config["name"]] = step_result
                    
                    # Stop on failure unless configured to continue
                    if not step_config.get("continue_on_failure", False):
                        break
            
            # Update execution status
            execution["status"] = WorkflowStatus.COMPLETED.value
            if execution["steps_failed"]:
                execution["status"] = WorkflowStatus.FAILED.value
            
        except Exception as e:
            execution["status"] = WorkflowStatus.FAILED.value
            execution["error"] = str(e)
            logger.error(f"Workflow execution failed: {e}")
        
        # Finalize execution
        execution["end_time"] = datetime.now().isoformat()
        
        # Update workflow metadata
        workflow["last_run"] = execution["end_time"]
        workflow["run_count"] += 1
        
        # Store history
        if workflow_id not in self.workflow_history:
            self.workflow_history[workflow_id] = []
        self.workflow_history[workflow_id].append(execution)
        
        # Cleanup old history (keep last 100)
        self.workflow_history[workflow_id] = self.workflow_history[workflow_id][-100:]
        
        logger.info(f"Workflow execution completed: {execution_id} - {execution['status']}")
        
        return execution
    
    async def _execute_step(self, 
                           step_config: Dict[str, Any],
                           previous_results: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step
        
        Args:
            step_config: Step configuration
            previous_results: Results from previous steps
            
        Returns:
            Step execution result
        """
        step_name = step_config["name"]
        action = step_config["action"]
        config = step_config["config"].copy()
        
        logger.info(f"Executing step: {step_name} ({action})")
        
        # Substitute variables from previous results
        config = self._substitute_variables(config, previous_results)
        
        try:
            # Execute action
            if action == "generate_content":
                result = await self._action_generate_content(config)
            elif action == "publish_to_cms":
                result = await self._action_publish_to_cms(config)
            elif action == "generate_variables":
                result = await self._action_generate_variables(config)
            elif action == "add_schema_markup":
                result = await self._action_add_schema_markup(config)
            elif action == "wait":
                result = await self._action_wait(config)
            elif action == "conditional":
                result = await self._action_conditional(config, previous_results)
            else:
                result = {"success": False, "error": f"Unknown action: {action}"}
            
            return result
            
        except Exception as e:
            logger.error(f"Step {step_name} failed: {e}")
            
            # Retry if configured
            if step_config.get("retry_on_failure", True):
                retries = 0
                max_retries = step_config.get("max_retries", 3)
                
                while retries < max_retries:
                    retries += 1
                    logger.info(f"Retrying step {step_name} (attempt {retries}/{max_retries})")
                    
                    await asyncio.sleep(5 * retries)  # Exponential backoff
                    
                    try:
                        return await self._execute_step(step_config, previous_results)
                    except:
                        continue
            
            return {"success": False, "error": str(e)}
    
    def _substitute_variables(self, 
                            config: Dict[str, Any],
                            context: Dict[str, Any]) -> Dict[str, Any]:
        """Substitute variables in configuration
        
        Variables format: {{step_name.field_name}}
        """
        import re
        
        def replace_var(match):
            var_path = match.group(1)
            parts = var_path.split('.')
            
            value = context
            for part in parts:
                if isinstance(value, dict) and part in value:
                    value = value[part]
                else:
                    return match.group(0)  # Keep original if not found
            
            return str(value)
        
        # Convert to string, replace, then parse back
        config_str = json.dumps(config)
        config_str = re.sub(r'\{\{([^}]+)\}\}', replace_var, config_str)
        
        return json.loads(config_str)
    
    async def _action_generate_content(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Action: Generate content pages"""
        try:
            # Get template and data
            template_id = config.get("template_id")
            project_id = config.get("project_id")
            limit = config.get("limit", 10)
            
            # Generate pages
            # This would integrate with your existing page generation logic
            pages_generated = []
            
            # Simulate generation
            for i in range(limit):
                page = {
                    "title": f"Generated Page {i+1}",
                    "content": "Generated content...",
                    "id": f"page_{i+1}"
                }
                pages_generated.append(page)
            
            return {
                "success": True,
                "data": {
                    "pages_generated": len(pages_generated),
                    "page_ids": [p["id"] for p in pages_generated]
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _action_publish_to_cms(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Action: Publish content to CMS"""
        try:
            cms_type = config.get("cms_type", "wordpress")
            page_ids = config.get("page_ids", [])
            
            # Get or create publisher
            publisher = self._get_publisher(cms_type, config.get("cms_config", {}))
            
            # Connect to CMS
            if not publisher.connect():
                return {"success": False, "error": "Failed to connect to CMS"}
            
            # Publish pages
            published_count = 0
            failed_count = 0
            
            for page_id in page_ids:
                # Get page data (would fetch from database)
                page_data = {"title": f"Page {page_id}", "content": "Content..."}
                
                success, response = publisher.publish_single(page_data)
                if success:
                    published_count += 1
                else:
                    failed_count += 1
            
            return {
                "success": True,
                "data": {
                    "published": published_count,
                    "failed": failed_count
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _action_generate_variables(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Action: Generate variables using AI"""
        try:
            # This would integrate with your variable generation logic
            variable_count = config.get("count", 10)
            
            variables = {
                "cities": [f"City {i+1}" for i in range(variable_count)],
                "services": [f"Service {i+1}" for i in range(variable_count)]
            }
            
            return {
                "success": True,
                "data": {
                    "variables": variables,
                    "total_combinations": variable_count * variable_count
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _action_add_schema_markup(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Action: Add schema markup to pages"""
        try:
            page_ids = config.get("page_ids", [])
            schema_type = config.get("schema_type", "Article")
            
            updated_count = 0
            
            for page_id in page_ids:
                # Get page data
                page_data = {"title": f"Page {page_id}", "content": "Content..."}
                
                # Generate schema
                schema = self.schema_generator.generate_schema(
                    content_type="generic",
                    page_data=page_data
                )
                
                # Update page with schema
                # This would update the database
                updated_count += 1
            
            return {
                "success": True,
                "data": {
                    "updated": updated_count
                }
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _action_wait(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Action: Wait for specified duration"""
        try:
            duration = config.get("seconds", 60)
            await asyncio.sleep(duration)
            
            return {
                "success": True,
                "data": {"waited": duration}
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def _action_conditional(self, 
                                 config: Dict[str, Any],
                                 context: Dict[str, Any]) -> Dict[str, Any]:
        """Action: Conditional execution based on previous results"""
        try:
            condition = config.get("condition", "")
            then_action = config.get("then")
            else_action = config.get("else")
            
            # Evaluate condition
            # Simple evaluation - could be enhanced
            condition_met = eval(condition, {"results": context})
            
            # Execute appropriate action
            if condition_met and then_action:
                return await self._execute_step(then_action, context)
            elif not condition_met and else_action:
                return await self._execute_step(else_action, context)
            
            return {"success": True, "data": {"condition_met": condition_met}}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_publisher(self, cms_type: str, config: Dict[str, Any]):
        """Get or create CMS publisher instance"""
        key = f"{cms_type}_{json.dumps(config, sort_keys=True)}"
        
        if key not in self.publishers:
            if cms_type == "wordpress":
                self.publishers[key] = WordPressPublisher(config)
            elif cms_type == "webflow":
                self.publishers[key] = WebflowPublisher(config)
            else:
                raise ValueError(f"Unknown CMS type: {cms_type}")
        
        return self.publishers[key]
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow status and history"""
        if workflow_id not in self.workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.workflows[workflow_id]
        history = self.workflow_history.get(workflow_id, [])
        
        return {
            "workflow": workflow,
            "history": history[-10:],  # Last 10 executions
            "stats": self._calculate_workflow_stats(history)
        }
    
    def _calculate_workflow_stats(self, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate workflow execution statistics"""
        if not history:
            return {"total_runs": 0}
        
        total = len(history)
        successful = sum(1 for h in history if h["status"] == WorkflowStatus.COMPLETED.value)
        failed = sum(1 for h in history if h["status"] == WorkflowStatus.FAILED.value)
        
        # Average duration
        durations = []
        for h in history:
            if "start_time" in h and "end_time" in h:
                start = datetime.fromisoformat(h["start_time"])
                end = datetime.fromisoformat(h["end_time"])
                durations.append((end - start).total_seconds())
        
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "total_runs": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0,
            "average_duration_seconds": avg_duration
        }