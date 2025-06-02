import os
import ollama
from ollama import GenerateResponse
from lib.app_logger import logger

ollama_model_name = os.environ.get("OLLAMA_MODEL", "gemma3:1b")
OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL", "http://localhost:11434")

ollama_client = ollama.Client(host=OLLAMA_API_URL)
# ollama_client.pull(ollama_model_name) # Pull the model if not already available (docker compose should automatically pull it)

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

def generate_search_queries(keywords, num_queries=3):
    """
    Genera query di ricerca usando un modello AI locale di Ollama basate su keywords estratte.

    Args:
        keywords: Lista di tuple (keyword, score)
        num_queries: Numero di query da generare

    Returns:
        Lista di query ottimizzate per la ricerca YouTube
    """
    # Estrai le keywords dalle tuple (keyword, score)
    kw_list = [kw for kw, _ in keywords]

    # Prepara il prompt per il modello
    prompt = f"""
    Genera {num_queries} query di ricerca per YouTube per trovare video educativi 
    basati sulle seguenti parole chiave estratte da appunti di studio:
    {', '.join(kw_list)}
    
    Ogni query deve:
    - Essere strutturata per massimizzare la rilevanza dei risultati su YouTube
    - Includere le parole chiave più importanti
    - Essere comprensibile anche senza contesto
    - Essere in italiano oppure in inglese
    - Mantenere una lunghezza ragionevole (3-7 parole)
    
    Restituisci SOLO le query generate, una per riga, senza numerazione o altro testo.
    NON numerare le query.
    """
    try:
        generated_response: GenerateResponse= ollama_client.generate(prompt=prompt, model=ollama_model_name, stream=False, keep_alive=60 * 10)
        generated_text = generated_response.response

        # Dividi il testo in righe e pulisci
        queries = [line.strip() for line in generated_text.split('\n') if line.strip()]
        # Se la query inizia con (numero.) rimuovilo
        queries = [q[2:].strip() if q and len(q) > 1 and q[0].isdigit() and q[1] == '.' else q for q in queries]

        # Gestisci il numero di query
        if len(queries) < num_queries:
            # Aggiungi keywords dirette se il modello ha generato meno query
            additional_queries = [kw for kw, _ in keywords[:(num_queries-len(queries))]]
            queries.extend(additional_queries)
        elif len(queries) > num_queries:
            queries = queries[:num_queries]
        return queries

    except Exception as e:
        logger.error(f"Error generating search queries: {e}, ollama_url: {OLLAMA_API_URL}, model: {ollama_model_name}")
        # Fallback all'approccio semplice in caso di errore
        fallback_queries = []
        for keyword, _ in keywords[:num_queries]:
            fallback_queries.append(f"{keyword}")
        return fallback_queries