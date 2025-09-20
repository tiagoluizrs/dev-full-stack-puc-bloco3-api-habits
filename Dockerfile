# Imagem base
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instalar dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor a porta da API-habit (ex: 5001)
EXPOSE 5001

# Comando para rodar a aplicação
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]