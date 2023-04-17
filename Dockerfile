FROM python:3.9.2-alpine3.13 AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 514/UDP

CMD [ "python", "-u", "server.py" ]