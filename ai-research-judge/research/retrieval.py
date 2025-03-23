import requests
from typing import List
import json
import os
from scholarly import scholarly
import time

# Import our data models
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.data_models import ResearchEvidence, ResearchSource, Query

def search_academic_literature(query: Query) -> List[ResearchEvidence]:
    """Search academic literature using Google Scholar API"""
    evidence_list = []
    try:
        search_query = scholarly.search_pubs(query.question)
        
        # Get top N results
        for i in range(min(query.evidence_count, 10)):
            try:
                result = next(search_query)
                
                # Create source metadata
                source = ResearchSource(
                    title=result.get('bib', {}).get('title', 'Unknown Title'),
                    authors=[author for author in result.get('bib', {}).get('author', ['Unknown'])],
                    published_date=str(result.get('bib', {}).get('pub_year', 'Unknown')),
                    publication=result.get('bib', {}).get('venue', None),
                    url=result.get('pub_url', ''),
                    citation_count=result.get('num_citations', 0)
                )
                
                # Get abstract if available
                content = result.get('bib', {}).get('abstract', 'Abstract not available')
                
                # Calculate simple relevance score based on title and abstract match
                relevance_score = calculate_relevance(query.question, result)
                
                # Extract key findings
                key_findings = extract_key_findings(content)
                
                # Only include if above threshold
                if relevance_score >= query.confidence_threshold:
                    evidence = ResearchEvidence(
                        source=source,
                        content=content,
                        relevance_score=relevance_score,
                        key_findings=key_findings
                    )
                    evidence_list.append(evidence)
            except StopIteration:
                break
            except Exception as e:
                print(f"Error retrieving research: {e}")
                continue
    except Exception as e:
        print(f"Error in scholarly search: {e}")
        # Fallback to simulated results for demonstration
        evidence_list = get_simulated_results(query)
                
    return evidence_list

def search_arxiv(query: Query) -> List[ResearchEvidence]:
    """Search arXiv for relevant papers"""
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query.question}",
        "start": 0,
        "max_results": query.evidence_count
    }
    
    evidence_list = []
    
    try:
        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            print(f"Error from arXiv API: {response.status_code}")
            return get_simulated_results(query, source="arxiv")
        
        # In a real implementation, you would parse the XML response
        # For demonstration, returning simulated results
        evidence_list = get_simulated_results(query, source="arxiv")
        
    except Exception as e:
        print(f"Error in arXiv search: {e}")
        evidence_list = get_simulated_results(query, source="arxiv")
    
    return evidence_list

def search_domain_specific_database(query: Query) -> List[ResearchEvidence]:
    """Search domain-specific databases based on the query domain"""
    if query.domain == "medical":
        return search_pubmed(query)
    elif query.domain == "legal":
        return search_legal_database(query)
    elif query.domain == "technical":
        return search_technical_literature(query)
    else:
        # Fallback to general research
        return get_simulated_results(query, source=f"domain-{query.domain}")

def search_pubmed(query: Query) -> List[ResearchEvidence]:
    """Search PubMed for medical research"""
    # In a real implementation, you would use the PubMed API
    # For demonstration, returning simulated results
    return get_simulated_results(query, source="pubmed")

def search_legal_database(query: Query) -> List[ResearchEvidence]:
    """Search legal databases"""
    # In a real implementation, you would use a legal database API
    # For demonstration, returning simulated results
    return get_simulated_results(query, source="legal")

def search_technical_literature(query: Query) -> List[ResearchEvidence]:
    """Search technical literature"""
    # In a real implementation, you would use tech literature APIs
    # For demonstration, returning simulated results
    return get_simulated_results(query, source="technical")

def calculate_relevance(question: str, result: dict) -> float:
    """Simple relevance calculation based on keyword matching"""
    # In a real implementation, you'd use semantic similarity with embeddings
    keywords = question.lower().split()
    title = result.get('bib', {}).get('title', '').lower()
    abstract = result.get('bib', {}).get('abstract', '').lower()
    
    title_matches = sum(1 for keyword in keywords if keyword in title)
    abstract_matches = sum(1 for keyword in keywords if keyword in abstract)
    
    # Weight title matches higher than abstract matches
    score = (title_matches * 0.6 + abstract_matches * 0.4) / len(keywords)
    return min(score * 2, 1.0)  # Cap at 1.0, multiply by 2 to increase scores

def extract_key_findings(text: str) -> List[str]:
    """Extract key findings from research text"""
    # In a real implementation, this would use NLP or an LLM
    # For demonstration, return basic findings based on text length
    if not text or text == "Abstract not available":
        return ["No key findings available"]
    
    # Split by sentences and return a few as key findings
    sentences = text.split('. ')
    if len(sentences) <= 3:
        return [f"Finding: {text}"]
    
    return [f"Finding: {sentences[i]}." for i in range(min(3, len(sentences)))]

def get_simulated_results(query: Query, source: str = "general") -> List[ResearchEvidence]:
    """Generate simulated research results for demonstration purposes"""
    # This is a fallback function for demonstration when APIs aren't available
    results = []
    
    # Create some simulated research papers based on the query
    topics = query.question.lower().split()
    
    for i in range(query.evidence_count):
        # Alternate between supporting and opposing evidence
        supports = i % 3 != 0  # 2/3 support, 1/3 oppose
        
        source_obj = ResearchSource(
            title=f"{'Study' if i % 2 == 0 else 'Analysis'} of {' '.join(topics[:3])} in {query.domain.capitalize()} Context",
            authors=[f"Researcher {chr(65+i)}", f"Professor {chr(75+i)}"],
            published_date=f"202{i%3}",
            publication=f"{source.capitalize()} Journal of {query.domain.capitalize()} Research",
            url=f"https://example.org/{source}/{i}",
            citation_count=50 - (i * 7)
        )
        
        # Create content that either supports or opposes the query
        if supports:
            content = f"Our research strongly indicates that {query.question}. Multiple experiments confirm this finding across different conditions."
            key_findings = [
                f"Strong evidence supporting {' '.join(topics[:2])}",
                f"Consistent results across {i+3} experiments",
                f"Findings have been replicated by other researchers"
            ]
        else:
            content = f"Contrary to popular belief, our research suggests that {query.question} may not be accurate. Several experiments failed to replicate previously reported effects."
            key_findings = [
                f"Limited evidence for {' '.join(topics[:2])}",
                f"Inconsistent results in {i+2} experiments",
                f"Methodological limitations in previous studies"
            ]
        
        # Calculate a realistic relevance score
        relevance_score = 0.95 - (i * 0.07)
        
        evidence = ResearchEvidence(
            source=source_obj,
            content=content,
            relevance_score=relevance_score,
            key_findings=key_findings
        )
        
        results.append(evidence)
    
    return results

def gather_evidence(query: Query) -> List[ResearchEvidence]:
    """Gather evidence from multiple sources"""
    # Gather evidence from different sources
    academic_evidence = search_academic_literature(query)
    arxiv_evidence = search_arxiv(query)
    domain_evidence = search_domain_specific_database(query)
    
    # Combine and sort by relevance
    all_evidence = academic_evidence + arxiv_evidence + domain_evidence
    sorted_evidence = sorted(all_evidence, key=lambda x: x.relevance_score, reverse=True)
    
    # Return top N most relevant pieces
    return sorted_evidence[:query.evidence_count]

# For testing
if __name__ == "__main__":
    test_query = Query(
        question="Does coffee consumption reduce the risk of Parkinson's disease?",
        domain="medical",
        confidence_threshold=0.5,
        evidence_count=3
    )
    
    evidence = gather_evidence(test_query)
    
    print(f"Found {len(evidence)} pieces of evidence:")
    for i, e in enumerate(evidence, 1):
        print(f"\n{i}. {e.source.title} ({e.source.published_date})")
        print(f"   Relevance: {e.relevance_score}")
        print(f"   Source: {e.source.publication}")
        print(f"   Content: {e.content[:100]}...")
        print(f"   Key Findings: {', '.join(e.key_findings)}")
