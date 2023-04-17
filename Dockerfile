FROM python:3.9.2-alpine3.13 as builder


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Test stage
FROM builder AS tester
WORKDIR /app
RUN python -m unittest discover -s . -p "*_test.py"

# Production stage
FROM python:3.9.2-alpine3.13 as final

RUN apk update && apk upgrade && \
    apk add --no-cache git
WORKDIR /app
COPY --from=tester /app .
EXPOSE 514/UDP

CMD [ "python", "-u", "server.py" ]