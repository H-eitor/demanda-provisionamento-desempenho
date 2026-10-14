#!/bin/bash

WORKERS=$1
CENARIO=$2

if [ -z "$WORKERS" ] || [ -z "$CENARIO" ]; then
    echo "Uso correto: ./iniciar.sh <num_workers> <nome_do_cenario>"
    exit 1
fi

cd ~/demanda-provisionamento-desempenho

echo "A iniciar a monitorização com top..."
# Grava CPU e RAM a cada 1 segundo em segundo plano
top -b -d 1 | grep --line-buffered "Cpu(s)\|MiB Mem" > "recursos_${CENARIO}.txt" &
TOP_PID=$!

echo "A iniciar o Uvicorn com $WORKERS worker(s)..."
uvicorn app.server:app --host 0.0.0.0 --port 8080 --workers $WORKERS

echo "A parar o servidor e a monitorização..."
kill $TOP_PID 2>/dev/null
echo "Gravação concluída! Ficheiro recursos_${CENARIO}.txt guardado."