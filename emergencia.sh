#!/bin/bash
export OLLAMA_MODELS="/media/astral/7DFD-F7FB/AI-O/models"

echo "🛑 Fechando instâncias antigas..."
pkill ollama 2>/dev/null

echo "🚀 Iniciando Servidor de IA Offline..."
/home/astral/.local/bin/ollama serve > /dev/null 2>&1 &
sleep 3

echo "🧠 Abrindo Llama 3..."
/home/astral/.local/bin/ollama run llama3
