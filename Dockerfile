# Stage 1: build environment
FROM python:3.9.2-alpine3.13 AS builder

RUN apk add gcc musl-dev && \
    pip install --upgrade setuptools
COPY . /app
WORKDIR /app
RUN ls
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m unittest discover -s . -p "*_test.py"

# Stage 2: production environment
FROM python:3.9.2-alpine3.13

WORKDIR /app
COPY --from=builder /wheels /wheels
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

COPY . /app

EXPOSE 514/UDP

CMD [ "python", "-u", "server.py" ]