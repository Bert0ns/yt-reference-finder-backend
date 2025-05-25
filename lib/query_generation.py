import os
import requests

OLLAMA_API_URL = os.environ.get("OLLAMA_API_URL")
ollama_model = os.environ.get("OLLAMA_MODEL", "gemma3:4b")

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
    """

    payload = {
        "model": ollama_model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(f"{OLLAMA_API_URL}/api/generate", json=payload)
        response.raise_for_status()

        # Estrai le query dalla risposta
        result = response.json()
        generated_text = result.get("response", "")

        # Dividi il testo in righe e pulisci
        queries = [line.strip() for line in generated_text.split('\n') if line.strip()]

        # Gestisci il numero di query
        if len(queries) < num_queries:
            # Aggiungi keywords dirette se il modello ha generato meno query
            additional_queries = [kw for kw, _ in keywords[:(num_queries-len(queries))]]
            queries.extend(additional_queries)
        elif len(queries) > num_queries:
            queries = queries[:num_queries]
        return queries

    except Exception as e:
        print(f"Errore durante l'utilizzo di Ollama: {e}")
        # Fallback all'approccio semplice in caso di errore
        fallback_queries = []
        for keyword, _ in keywords[:num_queries]:
            fallback_queries.append(f"{keyword}")
        return fallback_queries