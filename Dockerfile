# # Stage 1: build environment
# FROM python:3.9.2-alpine3.13 AS builder

# RUN apk add gcc musl-dev && \
#     pip install --upgrade setuptools
# COPY . /app
# WORKDIR /app
# RUN ls
# RUN pip install --no-cache-dir -r requirements.txt
# RUN python -m unittest discover -s . -p "*_test.py"

# # Stage 2: production environment
# FROM python:3.9.2-alpine3.13

# WORKDIR /app
# COPY --from=builder /wheels /wheels
# COPY ./requirements.txt /app/requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . /app

# EXPOSE 514/UDP

# CMD [ "python", "-u", "server.py" ]


FROM python:3.9.2-alpine3.13 as builder


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python -m unittest discover -s . -p "*_test.py"
# Test stage
FROM builder AS tester

WORKDIR /app

RUN python -m unittest discover -s . -p "*_test.py"

# Production stage
FROM python:3.9.2-alpine3.13 as final

RUN apk update && apk upgrade && \
    apk add --no-cache git

WORKDIR /app

COPY --from=builder /app .

EXPOSE 514/UDP

CMD [ "python", "-u", "server.py" ]