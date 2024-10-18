# Etapa 1: Usar uma imagem base Python com suporte ao sistema
FROM python:3.11.7-slim

# Definir o diretório de trabalho
WORKDIR /application

# Copiar o arquivo de requisitos e instalar dependências
COPY requirements.txt .

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    nginx \
    gcc \
    g++ \
    libblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar a aplicação Flask
COPY main.py /application
COPY build_user.py /application
COPY /app /application/app

# Copiar a configuração do NGINX personalizada
COPY nginx.conf /etc/nginx/nginx.conf

# Expor a porta 80 para o NGINX
EXPOSE 80

RUN flask db init
RUN flask db migrate -m 'migracao inicial'
RUN flask db upgrade
RUN python build_user.py


# Comando para iniciar o Gunicorn e NGINX
CMD gunicorn --bind 0.0.0.0:5000 main:application & nginx -g 'daemon off;'
