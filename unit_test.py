import unittest
from unittest.mock import patch, Mock
from server import trapHandler


class TestSyslogServer(unittest.TestCase):

    @patch('server.MongoClient')
    @patch('server.discordAlert')
    def test_trapHandler(self, mock_discord, mock_mongo):
        # Create a mock MongoDB client and collection
        mock_collection = Mock()
        mock_logs = Mock()
        trap = bytes(
            "<10>104: *Mar 22 21:29:10.128: %SYS-5-CONFIG_I: Configured from console by console", "utf-8")
        trap_log = 'INFO:server:Critical (2): <10>104: *Mar 22 21:29:10.128: %SYS-5-CONFIG_I: Configured from console by console from 127.0.0.1'
        client_ip = "127.0.0.1"
        # Send a syslog message to the server
        with self.assertLogs(level='INFO') as log:
            trapHandler(trap, client_ip)
            self.assertEqual(trap_log, log.output[0])


# if __name__ == '__main__':
#     unittest.main()
