import os
import ollama
from ollama import GenerateResponse

ollama_model_name = os.environ.get("OLLAMA_MODEL", "gemma3:4b")

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
        print(f"Using Ollama model '{ollama_model_name}' to generate queries with prompt:\n{prompt}")
        generated_response: GenerateResponse= ollama.generate(prompt=prompt, model=ollama_model_name, stream=False, keep_alive=60 * 10)
        generated_text = generated_response.response

        print(f"Generated response from Ollama: {generated_response}")

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
        print(f"Errore durante l'utilizzo di Ollama: {e}")
        # Fallback all'approccio semplice in caso di errore
        fallback_queries = []
        for keyword, _ in keywords[:num_queries]:
            fallback_queries.append(f"{keyword}")
        return fallback_queries