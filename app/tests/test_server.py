from socketserver import BaseServer, TCPServer
from unittest import main, TestCase
from threading import Thread
from mock import mock, patch
from server import main as server_main, ThreadedUDPRequestHandler


class ServerTestCase(TestCase):
    @mock.patch('os.environ.get', side_effect=['test_ip', '40479'])
    @patch.object(BaseServer, 'shutdown')
    @patch.object(TCPServer, 'server_bind')
    @patch.object(Thread, 'start')
    def test_starts(self, mock_start, *args):
        srv = server_main()
        srv.stop()
        mock_start.assert_called_once()
        self.assertEqual(srv.udp_ip, 'test_ip')
        self.assertEqual(srv.udp_port, 40479)


class HandlerTestCase(TestCase):
    @patch.object(ThreadedUDPRequestHandler, 'out')
    @patch.object(ThreadedUDPRequestHandler, 'convert', return_value='converted request')
    def test_prints_converted_message(self, mock_convert, mock_out):
        request = ['test request'.encode()]
        client_address = ['test_client_address', 45007]
        ThreadedUDPRequestHandler(request, client_address, None)
        mock_convert.assert_called_once_with('test request')
        mock_out.assert_called_once_with('converted request')

    @patch.object(ThreadedUDPRequestHandler, 'out')
    def test_logs_exceptions_bad_encoding(self, mock_out):
        request = ['test request']
        with self.assertLogs(level='ERROR') as logs:
            ThreadedUDPRequestHandler(request, None, None)
            self.assertEqual(len(logs.output), 1)
            self.assertEqual(logs.output[0].split('\n', 1)[0].split(':')[:2],
                             ['ERROR', 'root'])
            mock_out.assert_not_called()


    @patch.object(ThreadedUDPRequestHandler, 'convert', side_effect=Exception("Can't convert"))
    def test_logs_exceptions_bad_format(self, mock_convert):
        request = ['test request'.encode()]
        client_address = ['test_client_address', 45007]
        with self.assertLogs(level='ERROR') as logs:
            ThreadedUDPRequestHandler(request, client_address, None)
            self.assertEqual(len(logs.output), 1)
            self.assertEqual(logs.output[0].split('\n', 1)[0].split(':')[:2],
                             ['ERROR', 'root'])
            mock_convert.assert_called()


if __name__ == '__main__':
    main()
