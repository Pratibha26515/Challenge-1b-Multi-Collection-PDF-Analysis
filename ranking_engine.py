from sentence_transformers import SentenceTransformer, util

class RankingEngine:
    """Handles the loading of the model and ranking of text chunks."""
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """Initializes the model."""
        print("Loading ranking model...")
        self.model = SentenceTransformer(model_name)
        print("Model loaded.")

    def rank_chunks(self, chunks, persona, job_to_be_done):
        """
        Ranks text chunks based on semantic similarity to a synthesized query.

        Args:
            chunks (list): A list of text chunks from the PDF processor.
            persona (str): The user persona description.
            job_to_be_done (str): The task description.

        Returns:
            list: A sorted list of chunks with an added 'relevance_score'.
        """
        if not chunks:
            return []

        # Synthesize a detailed query from the persona and job
        synthesized_query = f"Query based on role and task. Role: {persona}. Task: {job_to_be_done}"

        # Create embeddings
        print("Creating embeddings for the query and document chunks...")
        query_embedding = self.model.encode(synthesized_query, convert_to_tensor=True)
        chunk_texts = [chunk['text'] for chunk in chunks]
        chunk_embeddings = self.model.encode(chunk_texts, convert_to_tensor=True)
        print("Embeddings created.")

        # Calculate cosine similarity
        cosine_scores = util.cos_sim(query_embedding, chunk_embeddings)

        # Add scores to chunks and sort
        for i in range(len(chunks)):
            chunks[i]['relevance_score'] = cosine_scores[0][i].item()
            
        ranked_chunks = sorted(chunks, key=lambda x: x['relevance_score'], reverse=True)
        
        return ranked_chunks