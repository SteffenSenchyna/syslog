# Syslog Server
This Python script implements a simple Syslog server that listens to incoming Syslog messages on port 514 and logs them to a MongoDB database. In addition, the script sends a notification to a Discord channel for Syslog messages with a severity level of 0-3 (Emergency, Alert, Critical, and Error).

## Prerequisites
* Python 3.7 or later
* A MongoDB database
* A Discord channel 

## Getting Started
To run this application, follow these steps:

* Clone this repository
* Install the required packages using pip install -r requirements.txt
* Run the application using python server.py
* The application will listen on port 514 for syslog messages

## Signal Handling
The server is designed to handle SIGTERM signals. When the server receives a SIGTERM signal, it will shut down gracefully.

## MongoDB Storage
Each incoming syslog message is stored in its own collection within the syslogs database, with the name of the collection being the IP address of the client that sent the message.

Discord Alerting
If the severity level of an incoming message is critical (severity <= 3), an alert will be sent to the Discord channel specified in the DISCORDURL environment variable. The alert will include the device IP address, severity level, and the message.

## Environmental Variables
```
MONGOURL=mongodb://localhost:27017/
DISCORDURL=https://discord.com/api/webhooks/<your_webhook_url>
```
