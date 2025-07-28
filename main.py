import json
import os
import argparse
from collections import defaultdict

from src.utils import get_timestamp
from src.pdf_processor import process_pdfs
from ranking_engine import RankingEngine

def run_analysis(input_path):
    """
    Main function to run the document intelligence pipeline.
    
    Args:
        input_path (str): Path to the input JSON file.
    """
    # 1. Load Input Data
    try:
        with open(input_path, 'r') as f:
            input_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {input_path}")
        return

    # Determine the base path for PDFs relative to the input file
    base_path = os.path.dirname(input_path)
    pdf_path = os.path.join(base_path, "PDFs")

    persona = input_data.get("persona", {}).get("role", "")
    job_to_be_done = input_data.get("job_to_be_done", {}).get("task", "")
    documents = input_data.get("documents", [])

    # 2. Process PDFs
    print("Starting PDF processing...")
    all_chunks = process_pdfs(documents, pdf_path)
    if not all_chunks:
        print("No text chunks were extracted. Exiting.")
        return
    print(f"Extracted {len(all_chunks)} text chunks.")

    # 3. Rank Content
    engine = RankingEngine()
    print("Ranking content based on persona and job...")
    ranked_chunks = engine.rank_chunks(all_chunks, persona, job_to_be_done)

    # 4. Structure the Output
    # Create subsection analysis from top 20 relevant chunks
    subsection_analysis = [
        {
            "document": chunk["document"],
            "refined_text": chunk["text"],
            "page_number": chunk["page_number"]
        }
        for chunk in ranked_chunks[:20]
    ]

    # Create section ranking
    section_scores = defaultdict(float)
    for chunk in ranked_chunks:
        section_key = (chunk["document"], chunk["section_title"], chunk["page_number"])
        # Use the highest score of any chunk in that section
        if chunk["relevance_score"] > section_scores[section_key]:
            section_scores[section_key] = chunk["relevance_score"]
    
    sorted_sections = sorted(section_scores.items(), key=lambda item: item[1], reverse=True)
    
    extracted_sections = [
        {
            "document": key[0],
            "section_title": key[1],
            "importance_rank": rank + 1,
            "page_number": key[2]
        }
        for rank, (key, score) in enumerate(sorted_sections)
    ]

    # 5. Assemble Final JSON
    output_data = {
        "metadata": {
            "input_documents": [doc.get("filename") for doc in documents],
            "persona": persona,
            "job_to_be_done": job_to_be_done,
            "processing_timestamp": get_timestamp()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    # 6. Save Output
    output_filename = os.path.join(base_path, "challenge1b_output.json")
    with open(output_filename, 'w') as f:
        json.dump(output_data, f, indent=2)
        
    print(f"Analysis complete. Output saved to {output_filename}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Persona-Driven Document Intelligence")
    parser.add_argument("input_json", help="Path to the input challenge1b_input.json file")
    args = parser.parse_args()
    
    run_analysis(args.input_json)