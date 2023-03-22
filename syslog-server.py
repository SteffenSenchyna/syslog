import errno
import logging
import logging.handlers
import socket
import socketserver
from pprint import pprint
from discord_webhook import DiscordEmbed, DiscordWebhook
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pymongo import MongoClient


class SysLogServer(socketserver.BaseRequestHandler):

    def handle(self):
        data = bytes.decode(self.request[0].strip())
        priority = int(data.split('<')[1].split('>')[0])
        severity = priority % 8
        level = logging.getLevelName(50 - severity * 10)
        # Get the client's IP address and port number
        client_ip = self.client_address[0]
        client_port = self.client_address[1]

        try:
            log = {
                "level": level,
                "severity":  severity,
                "message": data,
                "client_ip": client_ip,
                "created_at": datetime.utcnow(),
            }
            if severity <= 3:
                discordURL = "https://discord.com/api/webhooks/1088239694464168088/wNsQL0Pem8UAUrqpNKqfXSJwho4jExIPNGpXQGVn7txCUNpUm0e2uv879L3S3U84Iz8U"
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
                # add embed object to webhook
                webhook.add_embed(embed)
                webhook.execute()
            client = MongoClient('mongodb://localhost:27017/')
            logs = client["logs"]
            log_table = logs[client_ip]
            result = log_table.insert_one(log)
            if result.acknowledged != True:
                print("Could not upload Syslog message to DB")

        except Exception as e:
            print(e)
        # Log the incoming syslog message along with the client's IP address and port number
        print(f'{level} ({severity}): {data} from {client_ip}:{client_port}')


logging.basicConfig(level=logging.INFO)
port = 514
server = socketserver.ThreadingUDPServer(('0.0.0.0', port), SysLogServer)
print(f"Starting Syslog Server on Port:{port}")
print('--------------------------------------------------------------------------')
while True:
    try:
        server.handle_request()
    except KeyboardInterrupt:
        break
    except socket.error as e:
        if e.errno == errno.EINTR:
            continue
        else:
            raise
