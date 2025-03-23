import streamlit as st
import os
import time
from judge import research_judge
from models.data_models import Query, JudgmentDecision, ResearchEvidence, ResearchSource

# Set page configuration
st.set_page_config(
    page_title="AI Research Judge", 
    page_icon="📚",
    layout="wide"
)

# Apply custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .verdict-header {
        font-size: 1.8rem;
        font-weight: bold;
    }
    .verdict-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .confidence-meter {
        height: 30px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .supporting {
        background-color: #e8f5e9;
        border-left: 5px solid #4CAF50;
        padding: 10px;
        margin: 10px 0;
    }
    .opposing {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 10px;
        margin: 10px 0;
    }
    .conflict {
        background-color: #fff8e1;
        border-left: 5px solid #ffc107;
        padding: 10px;
        margin: 10px 0;
    }
    .citation {
        font-size: 0.9rem;
        color: #616161;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-header'>AI Research Judge</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Evidence-based answers to your research questions</p>", unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.header("Query Parameters")
    
    # Text input for research question
    question = st.text_area(
        "Research Question",
        placeholder="Does coffee consumption reduce the risk of Parkinson's disease?", 
        height=100
    )
    
    # Domain selection
    domain = st.selectbox(
        "Research Domain",
        options=["general", "medical", "physics", "psychology", "economics", "computer science", "biology", "chemistry"]
    )
    
    # Confidence threshold slider
    confidence_threshold = st.slider(
        "Confidence Threshold",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.05,
        help="Minimum confidence level required for evidence to be considered reliable"
    )
    
    # Evidence count
    evidence_count = st.number_input(
        "Number of Evidence Sources",
        min_value=1,
        max_value=10,
        value=5,
        help="Number of research papers to retrieve"
    )
    
    # API key input
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        help="Your OpenAI API key (required for the judgment process)"
    )
    
    # Submit button
    submit = st.button("📚 Get Research Judgment", type="primary")

# Check API key before proceeding
if submit:
    if not api_key:
        st.error("Please enter your OpenAI API key in the sidebar!")
    elif not question:
        st.error("Please enter a research question!")
    else:
        # Set API key
        os.environ["OPENAI_API_KEY"] = api_key
        
        # Create query
        query = Query(
            question=question,
            domain=domain,
            confidence_threshold=confidence_threshold,
            evidence_count=evidence_count
        )
        
        # Initialize judgment with default values in case of error
        judgment = JudgmentDecision(
            question=question,
            verdict="Unknown",
            confidence=0.0,
            reasoning="No analysis performed",
            supporting_evidence=[],
            opposing_evidence=[],
            limitations=["Analysis not performed due to error"]
        )
        
        # Display progress
        with st.status("Researching your question...", expanded=True) as status:
            st.write("Gathering research evidence...")
            time.sleep(1)  # Simulates the time it takes to gather evidence
            
            st.write("Analyzing evidence...")
            time.sleep(1)  # Simulates the time it takes to analyze evidence
            
            st.write("Formulating judgment...")
            time.sleep(1)  # Simulates the time it takes to formulate judgment
            
            # Get judgment from AI Research Judge
            try:
                judgment = research_judge(query)
                status.update(label="Research complete!", state="complete", expanded=False)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                # Continue with default judgment
        
        # Display results
        st.markdown("## Results")
        
        # Verdict card
        st.markdown("<div class='verdict-card'>", unsafe_allow_html=True)
        st.markdown(f"<h2 class='verdict-header'>Verdict: {judgment.verdict}</h2>", unsafe_allow_html=True)
        
        # Confidence meter
        st.markdown(f"**Confidence**: {judgment.confidence * 100:.1f}%")
        st.progress(judgment.confidence)
        
        # Reasoning
        st.markdown("### Reasoning")
        st.write(judgment.reasoning)
        
        # Key points section - only show if we have limitations to display as key points
        st.markdown("### Key Points")
        for limitation in judgment.limitations:
            st.markdown(f"- {limitation}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Evidence
        st.markdown("## Evidence Details")
        
        # Create tabs for different evidence categories
        tab1, tab2 = st.tabs(["Supporting Evidence", "Opposing Evidence"])
        
        with tab1:
            st.markdown("### Supporting Evidence")
            if not judgment.supporting_evidence:
                st.info("No supporting evidence found.")
            else:
                for evidence in judgment.supporting_evidence:
                    st.markdown(f"<div class='supporting'>", unsafe_allow_html=True)
                    st.markdown(f"**{evidence.source.title}**")
                    st.markdown(f"*{', '.join(evidence.source.authors)} ({evidence.source.published_date})*")
                    st.markdown(f"**Key Findings:**")
                    for finding in evidence.key_findings:
                        st.markdown(f"- {finding}")
                    st.markdown(f"**Relevance Score:** {evidence.relevance_score:.2f}")
                    st.markdown(f"<p class='citation'>{evidence.source.citation_count} citations | {evidence.source.publication}</p>", unsafe_allow_html=True)
                    if evidence.source.url:
                        st.markdown(f"[View Paper]({evidence.source.url})")
                    st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown("### Opposing Evidence")
            if not judgment.opposing_evidence:
                st.info("No opposing evidence found.")
            else:
                for evidence in judgment.opposing_evidence:
                    st.markdown(f"<div class='opposing'>", unsafe_allow_html=True)
                    st.markdown(f"**{evidence.source.title}**")
                    st.markdown(f"*{', '.join(evidence.source.authors)} ({evidence.source.published_date})*")
                    st.markdown(f"**Key Findings:**")
                    for finding in evidence.key_findings:
                        st.markdown(f"- {finding}")
                    st.markdown(f"**Relevance Score:** {evidence.relevance_score:.2f}")
                    st.markdown(f"<p class='citation'>{evidence.source.citation_count} citations | {evidence.source.publication}</p>", unsafe_allow_html=True)
                    if evidence.source.url:
                        st.markdown(f"[View Paper]({evidence.source.url})")
                    st.markdown("</div>", unsafe_allow_html=True)
        
        # Citations
        st.markdown("## Citations")
        for i, evidence in enumerate(judgment.supporting_evidence + judgment.opposing_evidence, 1):
            source = evidence.source
            st.markdown(f"<p class='citation'>{i}. {', '.join(source.authors)} ({source.published_date}). {source.title}. {source.publication}. {source.citation_count} citations.</p>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("AI Research Judge 2025 | Powered by Magentic and OpenAI")
