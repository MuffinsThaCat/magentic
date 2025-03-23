import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.data_models import ResearchEvidence, EvidenceAnalysis, Query
from typing import List, Dict, Any, cast
from magentic import prompt

@prompt("Analyze the following research evidence regarding the question: {question}\n\nEvidence title: {evidence.source.title}\nEvidence content: {evidence.content}\nEvidence key findings: {evidence.key_findings}\n\nDetermine whether this evidence supports or refutes the claim, and with what confidence. Explain your reasoning with key points and any limitations.")
def analyze_single_evidence(question: str, evidence: ResearchEvidence) -> EvidenceAnalysis:
    """Analyze a single piece of research evidence"""
    # This function is decorated with @prompt and will return an EvidenceAnalysis
    # For type checking, return a placeholder that won't be used
    return cast(EvidenceAnalysis, None)  # type: ignore

def analyze_all_evidence(query: Query, evidence_list: List[ResearchEvidence]) -> List[EvidenceAnalysis]:
    """Analyze each piece of evidence and its relevance to the question"""
    analysis_results = []
    
    for evidence in evidence_list:
        # When called, @prompt decorated functions return the result directly
        # For type checking, we need to cast the result
        analysis = cast(EvidenceAnalysis, analyze_single_evidence(query.question, evidence))
        analysis_results.append(analysis)
        
    return analysis_results

@prompt("Identify conflicts in the following evidence analyses for the question: {question}\n\nAnalyses: {analyses_str}\n\nList any contradictions or inconsistencies between different pieces of evidence.")
def identify_conflicts(question: str, analyses_str: str) -> List[str]:
    """Identify conflicts between different pieces of evidence"""
    # This function is decorated with @prompt and will return a List[str]
    # For type checking, return a placeholder that won't be used
    return cast(List[str], None)  # type: ignore

def format_analyses_for_conflict_check(analyses: List[EvidenceAnalysis]) -> str:
    """Format the analyses for the conflict check prompt"""
    result = ""
    for i, analysis in enumerate(analyses, 1):
        result += f"Analysis {i}:\n"
        result += f"- Supports claim: {analysis.supports_claim}\n"
        result += f"- Confidence: {analysis.confidence}\n"
        result += f"- Key points: {', '.join(analysis.key_points)}\n"
        result += f"- Limitations: {', '.join(analysis.limitations)}\n\n"
    return result

def analyze_evidence_batch(query: Query, evidence: List[ResearchEvidence]) -> Dict:
    """Analyze all gathered evidence and prepare for judgment"""
    # Analyze all evidence
    analyses = analyze_all_evidence(query, evidence)
    
    # Check for conflicts
    analyses_str = format_analyses_for_conflict_check(analyses)
    conflicts = cast(List[str], identify_conflicts(query.question, analyses_str))
    
    # Separate supporting and opposing evidence
    supporting = []
    opposing = []
    
    for i, analysis in enumerate(analyses):
        if analysis.supports_claim:
            supporting.append(evidence[i])
        else:
            opposing.append(evidence[i])
            
    return {
        "supporting_evidence": supporting,
        "opposing_evidence": opposing,
        "conflicts": conflicts,
        "analyses": analyses
    }

# For testing
if __name__ == "__main__":
    from models.data_models import ResearchSource
    
    # Create a test evidence piece
    source = ResearchSource(
        title="Effects of Coffee on Parkinson's Disease",
        authors=["Dr. Smith", "Dr. Johnson"],
        published_date="2022",
        publication="Journal of Neurology",
        url="https://example.com/coffee-parkinsons",
        citation_count=45
    )
    
    evidence = ResearchEvidence(
        source=source,
        content="Our research strongly indicates that coffee consumption reduces the risk of Parkinson's disease. Multiple experiments confirm this finding across different conditions.",
        relevance_score=0.92,
        key_findings=[
            "Coffee drinkers had 25% lower risk of Parkinson's",
            "Effect was dose-dependent",
            "Mechanism appears to be related to caffeine"
        ]
    )
    
    query = Query(
        question="Does coffee consumption reduce the risk of Parkinson's disease?",
        domain="medical"
    )
    
    # Cast the result to satisfy the type checker
    analysis = cast(EvidenceAnalysis, analyze_single_evidence(query.question, evidence))
    print(f"Supports claim: {analysis.supports_claim}")
    print(f"Confidence: {analysis.confidence}")
    print(f"Key points: {analysis.key_points}")
    print(f"Limitations: {analysis.limitations}")
