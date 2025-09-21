#!/bin/sh
# Aguarda o banco de dados ficar disponível
until pg_isready -h auth-db -p 5432 -U postgres; do
  echo "Aguardando o banco de dados..."
  sleep 2
done
exec "$@"

