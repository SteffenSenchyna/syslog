FROM python:3.9.2-alpine3.13

RUN apk add gcc musl-dev && \
    pip install --upgrade setuptools
COPY ./requirements.txt /app/requirements.txt
#Moove into the container app folder 
WORKDIR /app
# Install the required packages
RUN pip install -r requirements.txt
COPY . /app
EXPOSE 514/UDP

CMD [ "python", "-u", "server.py" ]
