from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from orchestrator import Orchestrator
from datetime import datetime
import uvicorn
import os

app = FastAPI(
    title="Co-op AI Management System",
    description="AI Operating System for Cooperatives and Cottage Industries",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

class OrderRequest(BaseModel):
    item_name: str
    quantity: int
    total_cost: float
    destination: str
    weight: float
    task_type: Optional[str] = None
    skill: Optional[str] = None
    order_type: Optional[str] = None
    location: Optional[str] = None
    action: Optional[str] = None
    category: Optional[str] = None
    product: Optional[str] = None

class AgentResponse(BaseModel):
    agent: str
    finding: str
    confidence: float
    details: Optional[dict] = None

class AnalysisResponse(BaseModel):
    agents: List[AgentResponse]
    recommendation: str
    risk_level: str
    risk_count: int
    confidence: float

class OrderResponse(BaseModel):
    can_proceed: bool
    finance: dict
    inventory: dict
    hr: dict
    logistics: dict
    compliance: dict
    rules: dict
    govt: dict

orchestrator = Orchestrator()

@app.get("/")
async def root():
    return {
        "name": "Co-op AI Management System",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "/": "GET - API information",
            "/health": "GET - Health check",
            "/analyze": "POST - Analyze a query",
            "/order": "POST - Analyze an order"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_query(request: QueryRequest):
    try:
        result = orchestrator.analyze_query(request.query)
        return AnalysisResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/order", response_model=OrderResponse)
async def analyze_order(request: OrderRequest):
    try:
        result = orchestrator.analyze_order(request.dict())
        return OrderResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
