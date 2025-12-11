#!/bin/bash
set -e

echo "Aguardando PostgreSQL estar pronto..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL está pronto!"

echo "Criando tabelas..."
uv run scripts/create_tables.py

if [ "$LOAD_SEED_DATA" = "true" ]; then
  echo "Carregando dados iniciais..."
  uv run scripts/load_data.py
fi

echo "Iniciando aplicação..."
exec "$@"
