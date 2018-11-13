#!/usr/bin/python
from Helper import Helper
from thread import start_new_thread
import socket


class Server(Helper):
    def __init__(self):
        super(Server, self).__init__()
        self.connections = dict()

    def __del__(self):
        '''
        disconnecting all connections and
        closing the socket when obj ending
        '''
        if hasattr(self, 'connections'):
            for client_ip in self.connections.keys():
                for client_con in self.connections[client_ip]:
                    self.disconnect_client(client_ip, client_con, if_log=False)
        super(Server, self).__del__()

    def create_server(self):
        '''
            bind the server to IP:PORT and start to listen
            IP and PORT is suppers attributes (getting from command line)
            if IP:PORT is invalid exit with ERROR code 1
        '''
        try:
            self.log('debug', "Creating server %s:%s..." % (self.ip, self.port))
            self.socket.bind((self.ip, self.port))
            self.socket.listen(100)
            self.socket.settimeout(1.0)
            self.log('debug', "Server is up and listening on %s:%s"
                            % (self.ip, self.port))
        except Exception as e:
            # The requested ip address or port is invalid
            self.log('error', "%s [%s:%s]" % (e, self.ip, self.port))
            exit(1)

    def menage_clients(self, func):
        '''
            accepting connections of clients to the server
            and making new thread for each connection
            each thread run
        '''
        try:
            while self.connection_up:
                client_con, addr = self.socket.accept()
                client_ip = addr[0]
                self.add_connection(client_ip, client_con)
                start_new_thread(func, (client_ip, client_con))
        except socket.timeout:
            self.menage_clients(func)
        except Exception:
            self.__del__()

    def add_connection(self, client_ip, client_con):
        if not client_ip in self.connections.keys():
            self.connections[client_ip] = list()
        self.connections[client_ip].append(client_con)
        self.log('debug', "%s is now connected..." % (client_ip))

    def disconnect_client(self, client_ip, client_con, if_log=True):
        '''
           remove disconnected client from the client list
        '''
        if hasattr(self, 'connections'):
            if client_ip in self.connections.keys():
                client_con.close()
                self.connections[client_ip].remove(client_con)
                if not len(self.connections[client_ip]):
                    del self.connections[client_ip]
                self.log('debug', "%s is now disconnected and removed from connection..." % (client_ip), if_log)

    def broadcast_message(self, message):
        '''
           broadcast massage
        '''
        self.log('debug', "broad cast to all: %s" % (message))
        for client_ip in self.connections.keys():
            for client_con in self.connections[client_ip]:
                try:
                    self.send_msg(client_ip, client_con, message)
                except:
                    self.log('debug', "cant send to %s - disconnecting" % (client_ip))
                    self.disconnect_client(client_ip, client_con)

    def server_down(self):
        self.connection_up = False

    def server_up(self):
        '''
        only creating server
        once you inhere from Server you may to"
        def server_up(self):
            super(Server, self).server_up()
            self.menage_clients(func)
        '''
        self.create_server()


if __name__ == '__main__':
    client = Server()
    client.server_up()
