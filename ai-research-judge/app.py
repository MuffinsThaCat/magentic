import os
import argparse
from models.data_models import Query
from judge import research_judge

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='AI Research Judge - Make evidence-based judgments on research questions')
    parser.add_argument('question', nargs='?', help='The research question to judge')
    parser.add_argument('--domain', '-d', default='general', help='Domain of the question (e.g., medical, legal, technical)')
    parser.add_argument('--confidence', '-c', type=float, default=0.7, help='Confidence threshold for evidence (0-1)')
    parser.add_argument('--evidence-count', '-e', type=int, default=5, help='Number of evidence pieces to gather')
    parser.add_argument('--interactive', '-i', action='store_true', help='Run in interactive mode')
    
    args = parser.parse_args()
    
    # Check for interactive mode or direct question
    if args.interactive:
        run_interactive_mode()
    elif args.question:
        process_question(args.question, args.domain, args.confidence, args.evidence_count)
    else:
        parser.print_help()

def run_interactive_mode():
    """Run the AI judge in interactive mode, asking questions and receiving judgments."""
    print("===== AI Research Judge =====")
    print("This system researches questions and provides evidence-based judgments.")
    print("Type 'exit' to quit.")
    print()
    
    while True:
        # Get user input
        question = input("Enter your research question: ").strip()
        if question.lower() == 'exit':
            print("Exiting AI Research Judge. Goodbye!")
            break
            
        domain = input("Domain (general, medical, legal, technical) [general]: ").strip() or "general"
        
        confidence_input = input("Confidence threshold (0-1) [0.7]: ").strip() or "0.7"
        try:
            confidence = float(confidence_input)
            if confidence < 0 or confidence > 1:
                print("Invalid confidence value. Using default 0.7.")
                confidence = 0.7
        except ValueError:
            print("Invalid confidence value. Using default 0.7.")
            confidence = 0.7
            
        evidence_input = input("Number of evidence pieces [5]: ").strip() or "5"
        try:
            evidence_count = int(evidence_input)
            if evidence_count < 1 or evidence_count > 20:
                print("Invalid evidence count. Using default 5.")
                evidence_count = 5
        except ValueError:
            print("Invalid evidence count. Using default 5.")
            evidence_count = 5
            
        # Process the question
        process_question(question, domain, confidence, evidence_count)
        
        print("\n" + "-" * 50 + "\n")

def process_question(question, domain, confidence, evidence_count):
    """Process a single question and display the judgment."""
    print(f"\nResearching: '{question}'")
    print(f"Domain: {domain}")
    print(f"Gathering evidence... (this may take a moment)")
    
    # Create the query
    query = Query(
        question=question,
        domain=domain,
        confidence_threshold=confidence,
        evidence_count=evidence_count
    )
    
    try:
        # Get the judgment
        judgment = research_judge(query)
        
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
            
    except Exception as e:
        print(f"Error processing judgment: {str(e)}")

if __name__ == "__main__":
    # Check if API key is set
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable is not set.")
        print("You can set it by running: export OPENAI_API_KEY='your-api-key'")
    
    main()
