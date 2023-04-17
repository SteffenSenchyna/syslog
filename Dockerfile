FROM python:3.9.2-alpine3.13 AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Production stage
FROM python:3.9.2-alpine3.13 as final

RUN apk update && apk upgrade 
WORKDIR /app
COPY --from=builder /app .
EXPOSE 514/UDP

CMD [ "python", "-u", "server.py" ]