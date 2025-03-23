# AI Research Judge

A generalizable AI judge system that accesses relevant research to make evidence-based decisions. Built with the Magentic framework for structured outputs and function calling capabilities.

## Features

- **Evidence Retrieval**: Gathers evidence from multiple sources, including Google Scholar and arXiv
- **Evidence Analysis**: Analyzes the gathered evidence to determine its relevance and identify any conflicts
- **Judgment Decision**: Produces a verdict based on the evidence, including confidence levels and reasoning
- **Interactive Mode**: Allows users to ask questions and receive judgments dynamically

## Setup

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install magentic openai pydantic scholarly requests
```

3. Set your OpenAI API key:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### Command-line mode

```bash
python app.py "Does coffee consumption reduce the risk of Parkinson's disease?" --domain medical
```

Optional parameters:
- `--domain`: Specify a research domain (e.g., medical, physics, economics)
- `--confidence`: Set the minimum confidence threshold (0.0-1.0)
- `--evidence-count`: Specify the number of evidence pieces to gather

### Interactive mode

```bash
python app.py --interactive
```

## Project Structure

- **models/data_models.py**: Pydantic data models for queries, research sources, evidence, analyses, and judgments
- **research/retrieval.py**: Functions to retrieve research evidence from academic sources
- **analysis/evidence_analyzer.py**: Functions to analyze the evidence, determine its relevance, and identify conflicts
- **judge.py**: Coordinates the retrieval and analysis of evidence to produce a final judgment
- **app.py**: Command-line interface for interacting with the AI judge

## Example Output

```
Query: Does coffee consumption reduce the risk of Parkinson's disease?
Domain: medical
Research sources: 5 papers found
Supporting evidence: 3 papers
Opposing evidence: 2 papers
Conflicts identified: 1 significant conflict regarding dosage effects
Judgment: Evidence SUPPORTS the claim with 75% confidence
Key points:
- Multiple studies show 25-30% risk reduction in coffee drinkers
- Effect appears dose-dependent and related to caffeine
- Larger, more recent studies show stronger effects
```

## Dependencies

- **Magentic**: Framework for integrating LLMs and managing function calls
- **Pydantic**: Data validation and serialization
- **Scholarly**: Library for retrieving academic papers from Google Scholar
- **Requests**: Making HTTP requests to external APIs
- **OpenAI**: Language model for evidence analysis and judgment generation
