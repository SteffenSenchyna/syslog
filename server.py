import errno
import logging
import logging.handlers
import signal
import socket
import socketserver
import time
from discord_webhook import DiscordEmbed, DiscordWebhook
from dotenv import load_dotenv
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# lsof -i :514


def severityLevel(argument):
    severityLabel = {
        0: "Emergency",
        1: "Alert",
        2: "Critical",
        3: "Error",
        4: "Warning",
        5: "Notification",
        6: "Informational"
    }
    return severityLabel.get(argument, "Default case")


def discordAlert(data, client_ip, severity):
    try:
        discordURL = os.environ["DISCORDURL"]
        webhook = DiscordWebhook(
            url=discordURL)
        embed = DiscordEmbed(
            title='Syslog Event', description=f'The following network device had a syslog event with a severity of {severity}', color='E33900')
        embed.set_author(name='NetBot',
                         icon_url='https://avatars0.githubusercontent.com/u/14542790')
        embed.set_footer(text='Network Syslog Event')
        embed.set_timestamp()
        embed.add_embed_field(
            name='Device', value=client_ip)
        embed.add_embed_field(
            name='Message', value=data, inline=False)
        webhook.add_embed(embed)
        webhook.execute()
    except Exception as e:
        log.error(str(e))


def trapHandler(trap, client_ip):
    def severityLevel(argument):
        severityLabel = {
            0: "Emergency",
            1: "Alert",
            2: "Critical",
            3: "Error",
            4: "Warning",
            5: "Notification",
            6: "Informational"
        }
        return severityLabel.get(argument, "Default case")
    data = bytes.decode(trap.strip())
    priority = int(data.split('<')[1].split('>')[0])
    severity = priority % 8
    # Get the client's IP address and port number
    log.info(
        f'{severityLevel(severity)} ({severity}): {data} from {client_ip}')
    try:
        syslog_trap = {
            "level": severityLevel(severity),
            "severity":  severity,
            "message": data,
            "client_ip": client_ip,
            "created_at": datetime.utcnow(),
        }
        if severity <= 3:
            discordAlert(data, client_ip, severity)

        mongoURL = os.environ["MONGOURL"]
        url = f"mongodb://{mongoURL}/"
        client = MongoClient(url)
        logs = client["syslogs"]
        log_table = logs[client_ip]
        result = log_table.insert_one(syslog_trap)
        if result.acknowledged != True:
            log.error("Could not upload Syslog trap to MongoDB")

        log.info(
            f"Successfully posted to MongoDB")

    except Exception as e:
        log.error(str(e))


class SysLogHandler(socketserver.BaseRequestHandler):
    def handle(self):
        trapHandler(self.request[0], self.client_address[0])


if __name__ == "__main__":
    load_dotenv()
    port = 514
    server = socketserver.ThreadingUDPServer(
        ('0.0.0.0', port), SysLogHandler)
    print(f"Starting Syslog Server on Port:{port}")
    print(
        '--------------------------------------------------------------------------')
    # Define the signal handler function

    def signal_handler(sig, frame):
        server.shutdown()

    # Register the signal handler for SIGTERM
    signal.signal(signal.SIGTERM, signal_handler)

    # Wait for incoming requests until a SIGTERM signal is received
    while True:
        try:
            server.handle_request()
        except KeyboardInterrupt:
            break
        except socket.error as e:
            if e.errno == errno.EINTR:
                continue
    print('Stopping Syslog Server')
    server.server_close()
    exit(0)
