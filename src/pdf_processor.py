import fitz  # PyMuPDF
import os

def process_pdfs(document_infos, base_pdf_path):
    """
    Extracts structured text chunks from a list of PDF documents.

    Args:
        document_infos (list): A list of dictionaries, each with a 'filename'.
        base_pdf_path (str): The path to the directory containing the PDFs.

    Returns:
        list: A list of dictionaries, where each represents a text chunk.
    """
    all_chunks = []
    
    for doc_info in document_infos:
        filename = doc_info.get("filename")
        if not filename:
            continue
            
        file_path = os.path.join(base_pdf_path, filename)
        
        try:
            doc = fitz.open(file_path)
        except Exception as e:
            print(f"Warning: Could not open or process {filename}. Error: {e}")
            continue

        current_section_title = "Introduction" # Default section title
        
        for page_num, page in enumerate(doc, start=1):
            # Get text blocks in a simpler way
            blocks = page.get_text("dict")["blocks"]
            
            for block in blocks:
                if "lines" not in block:
                    continue
                
                for line in block["lines"]:
                    # Simple heuristic: treat lines with bold font as potential section titles
                    is_title = False
                    if line["spans"]:
                        # Check for bold flag (bit 4) or larger font size
                        span = line["spans"][0]
                        if span.get("flags", 0) & 2**4 or span.get("size", 0) > 12:  # Bold or large font
                           current_section_title = span["text"].strip()
                           is_title = True
                           
                    # We add the paragraph text as a chunk, but not the title itself
                    if not is_title:
                        text = " ".join([span["text"] for span in line["spans"]]).strip()
                        if text: # Only add non-empty text chunks
                            chunk = {
                                "document": filename,
                                "page_number": page_num,
                                "section_title": current_section_title,
                                "text": text
                            }
                            all_chunks.append(chunk)
        doc.close()
        
    return all_chunks