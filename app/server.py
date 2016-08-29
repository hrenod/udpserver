import os
import threading
import socketserver
import logging
import signal

from converter import convert


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            data = self.request[0].decode()
        except Exception:
            logging.exception("Unable to decode input")
            return
        port = self.client_address[1]
        client_address = (self.client_address[0])
        cur_thread = threading.current_thread()
        logging.debug("thread %s" % cur_thread.name)
        logging.debug("received call from client address :%s" % client_address)
        logging.info("received data from port [%s]: %s" % (port, data))

        try:
            self.out(self.convert(data))
        except Exception as e:
            logging.exception("Unable to convert decoded string")

    @staticmethod
    def out(message):
        print(message)


    @staticmethod
    def convert(data):
        return convert(data)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


class Server():
    def __init__(self, udp_ip, udp_port):
        self.server = None
        self.server_thread = None
        self.udp_ip = udp_ip
        self.udp_port = int(udp_port)

    def serve(self):
        server = ThreadedUDPServer((self.udp_ip, self.udp_port),
                                   ThreadedUDPRequestHandler)
        self.server = server
        self.server_thread = server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        signal.signal(signal.SIGINT, self.signal_handler)

    def stop(self):
        if self.server:
            self.server.shutdown()

    def wait(self):
        if self.server_thread:
            self.server_thread.join()

    def signal_handler(self, signal, frame):
        self.stop()


def main():
    udp_ip = os.environ.get("UDP_IP", "127.0.0.1")
    udp_port = os.environ.get("UDP_PORT", 5005)
    server = Server(udp_ip, udp_port)
    server.serve()
    return server


if __name__ == "__main__":
    main().wait()