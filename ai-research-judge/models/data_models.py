from pydantic import BaseModel, Field
from typing import List, Optional

class Query(BaseModel):
    """The user's query to be researched and judged."""
    question: str
    domain: str = "general"
    confidence_threshold: float = 0.7
    evidence_count: int = 5

class ResearchSource(BaseModel):
    """Source metadata for a piece of research."""
    title: str
    authors: List[str]
    published_date: str
    publication: Optional[str] = None
    url: str
    citation_count: Optional[int] = None

class ResearchEvidence(BaseModel):
    """A piece of research evidence with relevance information."""
    source: ResearchSource
    content: str
    relevance_score: float
    key_findings: List[str]

class EvidenceAnalysis(BaseModel):
    """Analysis of a single piece of evidence."""
    supports_claim: bool
    confidence: float
    key_points: List[str]
    limitations: List[str]

class JudgmentDecision(BaseModel):
    """The final judgment decision with supporting evidence."""
    question: str
    verdict: str
    confidence: float
    supporting_evidence: List[ResearchEvidence]
    opposing_evidence: List[ResearchEvidence]
    reasoning: str
    limitations: List[str]
    recommendation: Optional[str] = None
