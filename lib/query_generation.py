import os
import ollama
from ollama import GenerateResponse
from lib.app_logger import logger

ollama_model_name = os.environ.get("OLLAMA_MODEL", "gemma3:1b")
OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434")

ollama_client = ollama.Client(host=OLLAMA_API_URL)
# ollama_client.pull(ollama_model_name) # Pull the model if not already available (docker compose should pull it)

def check_ollama_connection_health():
    """
    Checks connection health between the Flask and Ollama services.

    Returns:
        bool: True if is healthy, False otherwise.
    """
    try:
        ollama_client.show(ollama_model_name)
        logger.info(f"Ollama connection health check successful, ollama_url: {OLLAMA_API_URL}, model: {ollama_model_name}")
        return True
    except Exception as e:
        logger.error(f"Error checking Ollama connection health: {e}, ollama_url: {OLLAMA_API_URL}, model: {ollama_model_name}")
        return False

def generate_search_queries(keywords, num_queries=3, query_language='it'):
    """
    Generate search queries using a local Ollama AI model based on extracted keywords.

    :param keywords: List of tuples (keyword, score)
    :param num_queries: Number of queries to generate
    :param query_language: Query language (default 'it' for Italian)

    Returns:
        List of optimized queries for YouTube search
    """
    # Extract keywords from (keyword, score) tuples
    kw_list = [kw for kw, _ in keywords]

    # Prepare the model prompt
    prompt = f"""
    Generate {num_queries} YouTube search queries to find educational videos
    based on the following keywords extracted from study notes:
    {', '.join(kw_list)}
    
    Each query must:
    - Be structured to maximize result relevance on YouTube
    - Include the most important keywords
    - Be understandable without additional context
    - Be in Italian or English
    - Keep a reasonable length (3-7 words)
    - Be written in the language defined by the ISO code {query_language}
    
    Return ONLY the generated queries, one per line, without numbering or extra text.
    Do NOT number the queries.
    """
    try:
        generated_response: GenerateResponse= ollama_client.generate(prompt=prompt, model=ollama_model_name, stream=False, keep_alive=60 * 10)
        generated_text = generated_response.response

        # Split and clean lines
        queries = [line.strip() for line in generated_text.split('\n') if line.strip()]
        # Strip leading numbering like "1." if present
        queries = [q[2:].strip() if q and len(q) > 1 and q[0].isdigit() and q[1] == '.' else q for q in queries]

        # Normalize query count
        if len(queries) < num_queries:
            # Add direct keywords if the model generated fewer queries
            additional_queries = [kw for kw, _ in keywords[:(num_queries-len(queries))]]
            queries.extend(additional_queries)
        elif len(queries) > num_queries:
            queries = queries[:num_queries]
        return queries

    except Exception as e:
        logger.error(f"Error generating search queries: {e}, ollama_url: {OLLAMA_API_URL}, model: {ollama_model_name}")
        # Fall back to a simple keyword approach on error
        fallback_queries = []
        for keyword, _ in keywords[:num_queries]:
            fallback_queries.append(f"{keyword}")
        return fallback_queries