FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código
COPY . .

# O Render ignora o EXPOSE, mas é bom manter por documentação
EXPOSE 8501

# ALTERAÇÃO AQUI: 
# Usamos 'sh -c' para que o comando consiga ler a variável de ambiente $PORT do Render.
# Adicionamos flags para evitar problemas de conexão (CORS/Xsrf).
CMD ["sh", "-c", "streamlit run app/streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false"]