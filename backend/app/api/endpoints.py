# backend/app/api/endpoints.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from app.core.db import get_db
from app.graph.workflow import research_pipeline
from app.services.vector_store import save_paper_with_chunks
from app.schemas.research import ResearchPaperMetadata

router = APIRouter(prefix="/api/research", tags=["Research Engine"])


class AnalyzeRequest(BaseModel):
    raw_ideology: str
    problem_statement: str
    proposed_approach: Optional[str] = ""
    user_provided_papers: Optional[List[ResearchPaperMetadata]] = []


@router.post("/analyze")
async def analyze_ideology(payload: AnalyzeRequest, db: Session = Depends(get_db)):
    initial_state = {
        "raw_ideology": payload.raw_ideology,
        "problem_statement": payload.problem_statement,
        "proposed_approach": payload.proposed_approach or "",
        "user_provided_papers": payload.user_provided_papers or [],
        "discovered_papers": [],
        "errors": [],
    }

    try:
        # Run LangGraph pipeline
        result = await research_pipeline.ainvoke(initial_state)

        # Persist discovered papers into PostgreSQL + pgvector
        saved_papers = []
        for p in result.get("discovered_papers", []):
            try:
                p_db = save_paper_with_chunks(db, p)
                saved_papers.append(p_db.id)
            except Exception as e:
                print(f"Paper DB error: {e}")

        return {
            "dna": result.get("dna"),
            "discovered_papers": result.get("discovered_papers"),
            "persisted_paper_ids": saved_papers,
            "research_gaps": result.get("research_gaps"),
            "errors": result.get("errors"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))