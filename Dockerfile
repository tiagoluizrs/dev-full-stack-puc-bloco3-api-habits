# Imagem base
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instalar dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Copiar script wait-for-db.sh
COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

# Expor a porta da API-habit (ex: 5001)
EXPOSE 5003

# RUN sleep 120 && echo "Aguardando 2 minutos antes de iniciar a aplicação, esperando o banco ser levantado..."

RUN chmod +x entrypoint.sh
# Comando para rodar a aplicação via entrypoint
ENTRYPOINT ["sh", "entrypoint.sh"]