"""API cost tracking service for monitoring API usage and costs."""
from typing import Dict, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from models import ApiCost, OperationType
import json

class CostTracker:
    """Tracks API costs for different providers and operations."""
    
    # Cost per 1K tokens for different providers and models
    PRICING = {
        "perplexity": {
            "sonar": {
                "input": 0.0001,  # $0.10 per 1M tokens
                "output": 0.0001  # $0.10 per 1M tokens
            },
            "sonar-pro": {
                "input": 0.001,   # $1.00 per 1M tokens
                "output": 0.001   # $1.00 per 1M tokens
            }
        },
        "openai": {
            "gpt-3.5-turbo": {
                "input": 0.0005,  # $0.50 per 1M tokens
                "output": 0.0015  # $1.50 per 1M tokens
            },
            "gpt-4": {
                "input": 0.01,    # $10 per 1M tokens
                "output": 0.03    # $30 per 1M tokens
            },
            "gpt-4-turbo": {
                "input": 0.001,   # $1 per 1M tokens
                "output": 0.003   # $3 per 1M tokens
            }
        },
        "anthropic": {
            "claude-3-haiku": {
                "input": 0.00025,  # $0.25 per 1M tokens
                "output": 0.00125  # $1.25 per 1M tokens
            },
            "claude-3-sonnet": {
                "input": 0.003,    # $3 per 1M tokens
                "output": 0.015    # $15 per 1M tokens
            },
            "claude-3-opus": {
                "input": 0.015,    # $15 per 1M tokens
                "output": 0.075    # $75 per 1M tokens
            }
        }
    }
    
    @classmethod
    def estimate_tokens(cls, text: str) -> int:
        """Estimate token count (rough approximation)."""
        # Rough estimate: 1 token ≈ 4 characters
        return len(text) // 4
    
    @classmethod
    def calculate_cost(
        cls,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int
    ) -> float:
        """Calculate cost based on provider, model, and token usage."""
        if provider not in cls.PRICING:
            return 0.0
            
        provider_models = cls.PRICING[provider]
        if model not in provider_models:
            # Try to find a default model for the provider
            if provider == "perplexity":
                model = "sonar"
            elif provider == "openai":
                model = "gpt-3.5-turbo"
            elif provider == "anthropic":
                model = "claude-3-haiku"
            else:
                return 0.0
        
        if model not in provider_models:
            return 0.0
            
        pricing = provider_models[model]
        input_cost = (input_tokens / 1000) * pricing["input"]
        output_cost = (output_tokens / 1000) * pricing["output"]
        
        return round(input_cost + output_cost, 6)
    
    @classmethod
    def track_api_call(
        cls,
        db: Session,
        project_id: str,
        operation_type: OperationType,
        provider: str,
        model: Optional[str] = None,
        input_text: Optional[str] = None,
        output_text: Optional[str] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        details: Optional[Dict] = None
    ) -> ApiCost:
        """Track an API call and calculate its cost."""
        # Estimate tokens if not provided
        if input_tokens is None and input_text:
            input_tokens = cls.estimate_tokens(input_text)
        if output_tokens is None and output_text:
            output_tokens = cls.estimate_tokens(output_text)
            
        input_tokens = input_tokens or 0
        output_tokens = output_tokens or 0
        total_tokens = input_tokens + output_tokens
        
        # Determine model if not provided
        if not model:
            if provider == "perplexity":
                model = "sonar"
            elif provider == "openai":
                model = "gpt-3.5-turbo"
            elif provider == "anthropic":
                model = "claude-3-haiku"
        
        # Calculate cost
        cost = cls.calculate_cost(provider, model, input_tokens, output_tokens)
        
        # Create cost record
        api_cost = ApiCost(
            project_id=project_id,
            operation_type=operation_type,
            provider=provider,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost=cost,
            details=details or {}
        )
        
        db.add(api_cost)
        db.commit()
        db.refresh(api_cost)
        
        return api_cost
    
    @classmethod
    def get_project_costs(
        cls,
        db: Session,
        project_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict:
        """Get cost summary for a project."""
        query = db.query(ApiCost).filter(ApiCost.project_id == project_id)
        
        if start_date:
            query = query.filter(ApiCost.created_at >= start_date)
        if end_date:
            query = query.filter(ApiCost.created_at <= end_date)
            
        costs = query.all()
        
        # Calculate summaries
        total_cost = sum(c.cost for c in costs)
        total_tokens = sum(c.total_tokens for c in costs)
        
        # Group by operation type
        by_operation = {}
        for cost in costs:
            op_type = cost.operation_type.value
            if op_type not in by_operation:
                by_operation[op_type] = {
                    "count": 0,
                    "cost": 0.0,
                    "tokens": 0
                }
            by_operation[op_type]["count"] += 1
            by_operation[op_type]["cost"] += cost.cost
            by_operation[op_type]["tokens"] += cost.total_tokens
        
        # Group by provider
        by_provider = {}
        for cost in costs:
            provider = cost.provider
            if provider not in by_provider:
                by_provider[provider] = {
                    "count": 0,
                    "cost": 0.0,
                    "tokens": 0
                }
            by_provider[provider]["count"] += 1
            by_provider[provider]["cost"] += cost.cost
            by_provider[provider]["tokens"] += cost.total_tokens
        
        return {
            "project_id": project_id,
            "total_cost": round(total_cost, 4),
            "total_tokens": total_tokens,
            "total_calls": len(costs),
            "by_operation": by_operation,
            "by_provider": by_provider,
            "period": {
                "start": start_date.isoformat() if start_date else None,
                "end": end_date.isoformat() if end_date else None
            }
        }
    
    @classmethod
    def get_all_projects_summary(
        cls,
        db: Session,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Dict]:
        """Get cost summary for all projects."""
        query = db.query(
            ApiCost.project_id,
            func.sum(ApiCost.cost).label("total_cost"),
            func.sum(ApiCost.total_tokens).label("total_tokens"),
            func.count(ApiCost.id).label("total_calls")
        ).group_by(ApiCost.project_id)
        
        if start_date:
            query = query.filter(ApiCost.created_at >= start_date)
        if end_date:
            query = query.filter(ApiCost.created_at <= end_date)
            
        results = query.all()
        
        summaries = []
        for result in results:
            summaries.append({
                "project_id": result.project_id,
                "total_cost": round(result.total_cost, 4),
                "total_tokens": result.total_tokens,
                "total_calls": result.total_calls
            })
            
        return sorted(summaries, key=lambda x: x["total_cost"], reverse=True)
    
    @classmethod
    def estimate_operation_cost(
        cls,
        operation_type: OperationType,
        provider: str = "perplexity",
        model: Optional[str] = None,
        count: int = 1
    ) -> Dict:
        """Estimate cost for an operation before executing it."""
        # Default model selection
        if not model:
            if provider == "perplexity":
                model = "sonar"
            elif provider == "openai":
                model = "gpt-3.5-turbo"
            elif provider == "anthropic":
                model = "claude-3-haiku"
        
        # Estimated tokens per operation (based on typical usage)
        estimates = {
            OperationType.BUSINESS_ANALYSIS: {
                "input": 500,
                "output": 2000
            },
            OperationType.TEMPLATE_GENERATION: {
                "input": 1000,
                "output": 3000
            },
            OperationType.VARIABLE_GENERATION: {
                "input": 800,
                "output": 2500
            },
            OperationType.PAGE_GENERATION: {
                "input": 1500,
                "output": 1000  # Per page
            },
            OperationType.CONTENT_ENRICHMENT: {
                "input": 500,
                "output": 800
            }
        }
        
        if operation_type not in estimates:
            return {
                "estimated_cost": 0.0,
                "note": "Unknown operation type"
            }
        
        est = estimates[operation_type]
        input_tokens = est["input"] * count
        output_tokens = est["output"] * count
        
        cost = cls.calculate_cost(provider, model, input_tokens, output_tokens)
        
        return {
            "operation": operation_type.value,
            "provider": provider,
            "model": model,
            "count": count,
            "estimated_input_tokens": input_tokens,
            "estimated_output_tokens": output_tokens,
            "estimated_total_tokens": input_tokens + output_tokens,
            "estimated_cost": round(cost, 4),
            "cost_per_item": round(cost / count if count > 0 else 0, 4)
        }