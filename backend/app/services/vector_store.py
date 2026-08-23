import os
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from google import genai

from app.models.paper import PaperModel, PaperChunkModel

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
genai_client = genai.Client(api_key=api_key)


def generate_embedding(text: str) -> List[float]:
    """Generates 768-dimensional embeddings using Gemini embedding models."""
    response = genai_client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
    )
    return response.embedding


def save_paper_with_chunks(db: Session, paper_data: Dict[str, Any]):
    """Persists paper metadata and generates vector chunks in PostgreSQL."""
    existing = db.query(PaperModel).filter(PaperModel.id == paper_data["paper_id"]).first()
    if existing:
        return existing

    paper = PaperModel(
        id=paper_data["paper_id"],
        title=paper_data["title"],
        authors=", ".join(paper_data.get("authors", [])),
        year=paper_data.get("year"),
        venue=paper_data.get("venue"),
        url=str(paper_data.get("url")) if paper_data.get("url") else None,
        citation_count=paper_data.get("citation_count", 0),
        abstract=paper_data.get("abstract"),
        is_user_uploaded=paper_data.get("is_user_uploaded", False),
    )
    db.add(paper)
    db.flush()

    # Create chunk from abstract for semantic retrieval
    if paper_data.get("abstract"):
        embedding = generate_embedding(paper_data["abstract"])
        chunk = PaperChunkModel(
            paper_id=paper.id,
            chunk_index=0,
            content=paper_data["abstract"],
            embedding=embedding,
        )
        db.add(chunk)

    db.commit()
    db.refresh(paper)
    return paper