from magentic import prompt_chain
from typing import Dict, List

# Import our modules
from models.data_models import Query, JudgmentDecision, ResearchEvidence, EvidenceAnalysis
from research.retrieval import gather_evidence
from analysis.evidence_analyzer import analyze_evidence_batch

@prompt_chain(
    "You are an objective research judge tasked with making a decision on: {query.question}\n"
    "Based ONLY on the evidence provided, form a judgment. "
    "If the evidence is inconclusive or contradictory, state so in your verdict. "
    "Your reasoning should cite specific pieces of evidence and their strengths or limitations. "
    "Be fair and balanced in your assessment.",
    functions=[gather_evidence, analyze_evidence_batch],
)
def research_judge(query: Query) -> JudgmentDecision: ...

# Example of how to use this in another file
if __name__ == "__main__":
    # Test the judge with a sample query
    test_query = Query(
        question="Does coffee consumption reduce the risk of Parkinson's disease?",
        domain="medical",
        confidence_threshold=0.5,
        evidence_count=5
    )
    
    # Get the judgment
    judgment = research_judge(test_query)
    
    # Display the results
    print("\n===== JUDGMENT =====")
    print(f"Question: {judgment.question}")
    print(f"Verdict: {judgment.verdict}")
    print(f"Confidence: {judgment.confidence}")
    
    print("\n===== REASONING =====")
    print(judgment.reasoning)
    
    print("\n===== SUPPORTING EVIDENCE =====")
    for i, evidence in enumerate(judgment.supporting_evidence, 1):
        print(f"{i}. {evidence.source.title} ({evidence.source.published_date})")
        print(f"   Relevance: {evidence.relevance_score}")
        print(f"   Key findings: {', '.join(evidence.key_findings)}")
    
    print("\n===== OPPOSING EVIDENCE =====")
    for i, evidence in enumerate(judgment.opposing_evidence, 1):
        print(f"{i}. {evidence.source.title} ({evidence.source.published_date})")
        print(f"   Relevance: {evidence.relevance_score}")
        print(f"   Key findings: {', '.join(evidence.key_findings)}")
    
    print("\n===== LIMITATIONS =====")
    for limitation in judgment.limitations:
        print(f"• {limitation}")
    
    if judgment.recommendation:
        print(f"\n===== RECOMMENDATION =====")
        print(judgment.recommendation)
