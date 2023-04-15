import errno
import logging
import logging.handlers
import socket
import socketserver
from discord_webhook import DiscordEmbed, DiscordWebhook
from dotenv import load_dotenv
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv


class SysLogServer(socketserver.BaseRequestHandler):

    def handle(self):
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
        load_dotenv()
        data = bytes.decode(self.request[0].strip())
        print(data)
        priority = int(data.split('<')[1].split('>')[0])
        severity = priority % 8
        # Get the client's IP address and port number
        client_ip = self.client_address[0]
        print(f'{severityLevel(severity)} ({severity}): {data} from {client_ip}')

        try:
            syslog_trap = {
                "level": severityLevel(severity),
                "severity":  severity,
                "message": data,
                "client_ip": client_ip,
                "created_at": datetime.utcnow(),
            }
            if severity <= 3:
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

            mongoURL = os.environ["MONGOURL"]
            url = f"mongodb://{mongoURL}/"
            client = MongoClient(url)
            logs = client["syslogs"]
            log_table = logs[client_ip]
            result = log_table.insert_one(syslog_trap)
            if result.acknowledged != True:
                print("Could not upload Syslog trap to DB")

            print(f"Posted to DB with id {result.inserted_id}\n{syslog_trap}")

        except Exception as e:
            print(e)
        # Log the incoming syslog message along with the client's IP address and port number


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
