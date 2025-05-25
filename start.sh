#!/bin/bash

ollama serve &
sleep 10
ollama pull gemma1:4b  # o il modello che usi
python app.py