# Persona-Driven Document Intelligence

This project is a document intelligence pipeline that processes collections of PDF documents, ranks their content based on a user persona and a specific job-to-be-done, and outputs structured, relevant information in JSON format. It is designed for scenarios where extracting and prioritizing information from large document sets is needed, such as travel planning, research, or business analysis.

## Features
- Extracts structured text chunks from multiple PDFs
- Ranks content using semantic similarity (Sentence Transformers)
- Persona and task-driven content extraction
- Outputs top relevant sections and detailed analysis in JSON
- CLI and Docker support

## Directory Structure
```
├── main.py                # Main entry point for running the pipeline
├── ranking_engine.py      # Ranks text chunks using sentence-transformers
├── src/
│   ├── pdf_processor.py   # Extracts text and sections from PDFs
│   └── utils.py           # Utility functions (e.g., timestamp)
├── requirements.txt       # Python dependencies
├── Dockerfile             # For containerized execution
├── Collection 1/          # Example input/output and PDFs
│   ├── challenge1b_input.json
│   ├── challenge1b_output.json
│   └── PDFs/
```

## Setup

### 1. Python (Local)
- Python 3.9+ recommended
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```
  (Ensure you have [PyTorch CPU wheels](https://download.pytorch.org/whl/cpu) if running on CPU.)

### 2. Docker
- Build the Docker image:
  ```bash
  docker build -t doc-intel .
  ```

## Usage

### Command Line
Run the pipeline with an input JSON file:
```bash
python main.py Collection\ 1/challenge1b_input.json
```

### Docker
```bash
docker run -v "$PWD/Collection 1:/app/Collection 1" doc-intel Collection\ 1/challenge1b_input.json
```

- The output will be saved as `challenge1b_output.json` in the same directory as the input.

## Input Format
Example (`challenge1b_input.json`):
```json
{
  "challenge_info": { ... },
  "documents": [
    { "filename": "South of France - Cities.pdf", "title": "South of France - Cities" },
    ...
  ],
  "persona": { "role": "Travel Planner" },
  "job_to_be_done": { "task": "Plan a trip of 4 days for a group of 10 college friends." }
}
```
- `documents`: List of PDFs to process (must be in a `PDFs/` subfolder next to the input JSON)
- `persona`: The user role (e.g., "Travel Planner")
- `job_to_be_done`: The specific task or goal

## Output Format
Example (`challenge1b_output.json`):
```json
{
  "metadata": {
    "input_documents": [ ... ],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip of 4 days for a group of 10 college friends.",
    "processing_timestamp": "..."
  },
  "extracted_sections": [
    { "document": "South of France - Things to Do.pdf", "section_title": "Introduction", "importance_rank": 1, "page_number": 1 },
    ...
  ],
  "subsection_analysis": [
    { "document": "South of France - Cities.pdf", "refined_text": "...", "page_number": 2 },
    ...
  ]
}
```

## How It Works
1. **PDF Extraction:** Extracts text and section titles from each PDF using heuristics (bold/large font for section titles).
2. **Ranking:** Uses a Sentence Transformer model to rank text chunks by relevance to the persona and job-to-be-done.
3. **Output:** Produces a JSON with ranked sections and detailed analysis.

## Dependencies
- PyMuPDF
- sentence-transformers
- torch (CPU)

## Example
See `Collection 1/challenge1b_input.json` and `Collection 1/challenge1b_output.json` for a full example.

## Team Coderzzz
