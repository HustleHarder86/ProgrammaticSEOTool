"""API routes for cost tracking functionality."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from cost_tracker import CostTracker, OperationType
from models import Project
from typing import Optional, List
from datetime import datetime, timedelta
from pydantic import BaseModel

# Create router
router = APIRouter(prefix="/api/costs", tags=["costs"])

class CostEstimateRequest(BaseModel):
    operation_type: str
    provider: str = "perplexity"
    model: Optional[str] = None
    count: int = 1

class CostSummaryResponse(BaseModel):
    project_id: str
    total_cost: float
    total_tokens: int
    total_calls: int
    by_operation: dict
    by_provider: dict
    period: dict

class ProjectCostSummary(BaseModel):
    project_id: str
    project_name: str
    total_cost: float
    total_tokens: int
    total_calls: int

@router.get("/estimate")
async def estimate_cost(
    operation: str = Query(..., description="Operation type"),
    provider: str = Query("perplexity", description="AI provider"),
    model: Optional[str] = Query(None, description="Model name"),
    count: int = Query(1, description="Number of operations")
):
    """Estimate cost for an operation before executing it."""
    try:
        # Convert string to enum
        operation_type = OperationType(operation)
        
        estimate = CostTracker.estimate_operation_cost(
            operation_type=operation_type,
            provider=provider,
            model=model,
            count=count
        )
        
        return estimate
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid operation type. Valid types: {[op.value for op in OperationType]}"
        )

@router.get("/projects/{project_id}", response_model=CostSummaryResponse)
async def get_project_costs(
    project_id: str,
    days: Optional[int] = Query(None, description="Number of days to look back"),
    db: Session = Depends(get_db)
):
    """Get cost summary for a specific project."""
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = None
    if days:
        start_date = end_date - timedelta(days=days)
    
    # Get cost summary
    summary = CostTracker.get_project_costs(
        db=db,
        project_id=project_id,
        start_date=start_date,
        end_date=end_date
    )
    
    return summary

@router.get("/projects", response_model=List[ProjectCostSummary])
async def get_all_projects_costs(
    days: Optional[int] = Query(None, description="Number of days to look back"),
    db: Session = Depends(get_db)
):
    """Get cost summary for all projects."""
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = None
    if days:
        start_date = end_date - timedelta(days=days)
    
    # Get cost summaries
    summaries = CostTracker.get_all_projects_summary(
        db=db,
        start_date=start_date,
        end_date=end_date
    )
    
    # Enrich with project names
    enriched_summaries = []
    for summary in summaries:
        project = db.query(Project).filter(Project.id == summary["project_id"]).first()
        enriched_summaries.append({
            **summary,
            "project_name": project.name if project else "Unknown Project"
        })
    
    return enriched_summaries

@router.get("/operations/{project_id}")
async def get_project_operations(
    project_id: str,
    limit: int = Query(100, description="Maximum number of operations to return"),
    offset: int = Query(0, description="Number of operations to skip"),
    db: Session = Depends(get_db)
):
    """Get detailed list of operations and their costs for a project."""
    from models import ApiCost
    
    # Check if project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get operations
    operations = db.query(ApiCost)\
        .filter(ApiCost.project_id == project_id)\
        .order_by(ApiCost.created_at.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()
    
    # Format response
    return {
        "project_id": project_id,
        "operations": [
            {
                "id": op.id,
                "operation_type": op.operation_type.value,
                "provider": op.provider,
                "model": op.model,
                "input_tokens": op.input_tokens,
                "output_tokens": op.output_tokens,
                "total_tokens": op.total_tokens,
                "cost": op.cost,
                "created_at": op.created_at.isoformat(),
                "details": op.details
            }
            for op in operations
        ],
        "total": db.query(ApiCost).filter(ApiCost.project_id == project_id).count()
    }

@router.get("/pricing")
async def get_pricing_info():
    """Get current pricing information for all providers."""
    return {
        "pricing": CostTracker.PRICING,
        "note": "Prices are per 1,000 tokens in USD"
    }