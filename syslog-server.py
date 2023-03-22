import logging
import logging.handlers
import socketserver


class SysLogServer(socketserver.BaseRequestHandler):
    def handle(self):
        data = bytes.decode(self.request[0].strip())
        priority = int(data.split('<')[1].split('>')[0])
        severity = priority % 8
        level = logging.getLevelName(50 - severity * 10)
        # Get the client's IP address and port number
        client_ip = self.client_address[0]
        client_port = self.client_address[1]

        # Log the incoming syslog message along with the client's IP address and port number
        print(f'{level} ({severity}): {data} from {client_ip}:{client_port}')


logging.basicConfig(level=logging.INFO)
server = socketserver.UDPServer(('0.0.0.0', 514), SysLogServer)
print("Starting Syslog Server")
server.serve_forever()
