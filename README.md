# Syslog Server
This Python script implements a simple Syslog server that listens to incoming Syslog messages on port 514 and logs them to a MongoDB database. In addition, the script sends a notification to a Discord channel for Syslog messages with a severity level of 0-3 (Emergency, Alert, Critical, and Error). This server is part of a larger project, which includes several microservices and other components that collectively provide tools to manage on-premise networking devices. The view the cluster architecture and the CI/CD pipeline for deployment, refer to the [Cluster Manifest Repository](https://github.com/SteffenSenchyna/cluster-chart).

## Prerequisites
* Python 3.7 or later
* A MongoDB database
* A Discord channel 

## Getting Started
To run this application, follow these steps:

* Clone this repository
* Install the required packages using `pip install -r requirements.txt`
* Run the application using `python server.py`
* The application will listen on port 514 for syslog messages

## Usage
Send a Syslog message to the server by running the following command in a separate terminal window:
```
echo "<13>Feb  5 17:32:18 mymachine myproc[10]: %% It's time to make the do-nuts." | nc -w 1 -u localhost 514
```

## Signal Handling
The server is designed to handle SIGTERM signals. When the server receives a SIGTERM signal, it will shut down gracefully.

## MongoDB Storage
Each incoming syslog message is stored in its own collection within the syslogs database, with the name of the collection being the IP address of the client that sent the message.

## Discord Alerting
If the severity level of an incoming message is critical (severity <= 3), an alert will be sent to the Discord channel specified in the DISCORDURL environment variable. The alert will include the device IP address, severity level, and the message.

## Environmental Variables
Create a .env file in the root directory of the project and set the following environment variables:
```
MONGOURL=<MongoDB URL>
DISCORDURL=https://discord.com/api/webhooks/<your_webhook_url>
```
