
FROM python:3.11.7-slim


WORKDIR /application

COPY requirements.txt .


RUN apt-get update && apt-get install -y \
    nginx \
    gcc \
    g++ \
    libblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py /application
COPY build_user.py /application
COPY /app /application/app

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

RUN flask db init
RUN flask db migrate -m 'migracao inicial'
RUN flask db upgrade
RUN python build_user.py

CMD gunicorn --bind 0.0.0.0:5000 main:application & nginx -g 'daemon off;'
