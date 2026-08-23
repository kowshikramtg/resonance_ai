from sqlalchemy import Column, String, Integer, Boolean, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.core.db import Base

class PaperModel(Base):
    __tablename__ = "papers"

    id = Column(String, primary_key=True, index=True)  # OpenAlex ID, DOI, or internal UUID
    title = Column(Text, nullable=False)
    authors = Column(Text)  # Stored as comma-separated or JSON string
    year = Column(Integer, nullable=True)
    venue = Column(String, nullable=True)
    url = Column(String, nullable=True)
    citation_count = Column(Integer, default=0)
    abstract = Column(Text, nullable=True)
    is_user_uploaded = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chunks = relationship("PaperChunkModel", back_populates="paper", cascade="all, delete-orphan")

class PaperChunkModel(Base):
    __tablename__ = "paper_chunks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    paper_id = Column(String, ForeignKey("papers.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    # Using 768-dim vectors (compatible with gemini-embedding-001 or BGE models)
    embedding = Column(Vector(768))

    paper = relationship("PaperModel", back_populates="chunks")