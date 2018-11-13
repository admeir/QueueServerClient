#!/usr/bin/python
from Helper import Helper
import select
import sys
import logging


class Client(Helper):
    def __init__(self):
        '''
        constructor
        '''
        Helper.LOGGER_NAEM = 'Client'
        super(Client, self).__init__()

    def conect_to_server(self):
        '''
        connecting to server
        Exit code 1 on exception
        '''
        try:
            logging.info("Connecting to server %s:%s..." % (self.ip_port_tup))
            self.socket.connect(self.ip_port_tup)
            logging.info("Connected")
        except Exception as e:
            logging.error(e)
            print("The ip address [%s:%s] is not reachable or is invalid" %
                  (self.ip_port_tup))
            exit(1)

    def cli(self):
        '''
            read/write messages from/to socket
            byebye - will disconnect the client from the chat room
        '''
        try:
            while self.connection_up:
                sockets_list = [sys.stdin, self.socket]
                read_sockets, write_socket, error_socket = \
                    select.select(sockets_list, [], [])
                for socks in read_sockets:
                    if socks == self.socket:
                        try:
                            _, _, message = self.get_msg('server', socks)
                            if len(message):
                                print 'RECEIVED: %s' %message
                                if message == "STOP":
                                    self.connection_up = False
                                    break
                        except Exception as e:
                            logging.error(e)
                            print("The ip address [%s:%s] is disconnected" %
                                  (self.ip_port_tup))
                            exit(1)
                    else:
                        message = sys.stdin.readline().strip()
                        if not len(message) == 0:
                            self.send_msg('server', self.socket, message)
        except Exception:
            pass

if __name__ == '__main__':
    client = Client()
    client.conect_to_server()
    client.cli()
