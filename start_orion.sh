#!/bin/bash

# Define o caminho dos modelos no seu HD Externo
export OLLAMA_MODELS="/media/astral/7DFD-F7FB/AI-O/models"

echo "🛑 [O.R.I.O.N.] Fechando instâncias antigas..."
pkill ollama 2>/dev/null

echo "🚀 [O.R.I.O.N.] Iniciando Servidor de IA Offline..."
/home/astral/.local/bin/ollama serve > /dev/null 2>&1 &
sleep 4 # Um segundo a mais para o servidor acordar 100%

echo "⚡ [O.R.I.O.N.] Sincronizando Sistemas e Inicializando Interface..."
# Executa a nossa mente em Python usando o python global (pois pendrives não aceitam venv)
python3.13 /media/astral/7DFD-F7FB/AI-O-Go/a.py
