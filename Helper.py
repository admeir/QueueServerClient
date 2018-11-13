from argparse import ArgumentParser
import socket
import os
import logging
import datetime
import signal
import threading
import json

class HelperErr(Exception):
    def __init__(self, message):
        super(HelperErr, self).__init__("ERROR:%s" % message)


class Helper(object):
    SOCK_SIZE = 2048
    LOGGER_NAEM = 'Helper'

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.get_args()
        self.log_sem = threading.Semaphore()
        self.ip_port_tup = (self.ip, self.port)
        self.create_logger()
        self.connection_up = True
        signal.signal(signal.SIGINT, self.signal_handler)

    def __del__(self):
        if hasattr(self, 'socket'):
            self.log(None, 'closing Socket...', if_log=False)
            self.socket.close()
            self.log(None, 'Socket closed', if_log=False)

    def signal_handler(self, sig, frame):
        self.server_up = False

    def get_args(self):
        '''
        parsing args from cli
        :return:
        '''
        parser = ArgumentParser()
        parser.add_argument(
            '--ip', action="store", dest='ip',
            help='SERVER IP ADDRESS', required=True)
        parser.add_argument(
            '--port', action="store", dest='port',
            help='SERVER PORT', required=True)
        help = '''Path to logingd directory.
        the default is run path: %s (run directory)''' % (os.getcwd())
        help = 'loging levels: INFO, DEBUG'
        parser.add_argument('--log_level', action="store", dest='log_level',
                            help=help, default='INFO')
        args = parser.parse_args()
        self.ip = args.ip
        self.port = int(args.port)
        self.log_level = logging.DEBUG
        self.validate_args()

    def validate_ip(self):
        ip_parts = self.ip.split('.')
        if len(ip_parts) not in [4, 6]:
            return False
        for part in ip_parts:
            try:
                int(part)
            except ValueError:
                return False
        return True

    def validate_args(self):
        if not self.validate_ip():
            raise HelperErr("ip address isn't valid")

    def create_logger(self):
        '''
        name from : Helper.log_name
        :return:
        '''
        logs_path = os.path.join(os.path.dirname(
                                 os.path.realpath(__file__)),
                                 'logs')
        if not os.path.exists(logs_path):
            os.makedirs(logs_path)

        if not os.path.exists(logs_path):
            os.makedirs(logs_path)
        log_path = os.path.join(logs_path, '%s.log' % Helper.LOGGER_NAEM)
        logging.basicConfig(filename=log_path,
                            level=logging.DEBUG,
                            filemode='w')

    def change_log_level(self, log_level):
        '''
        :param log_level: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
        :return: None
        changing log level
        '''
        logging.getLogger().setLevel(getattr(logging, log_level))

    def log(self, log_level, msg, if_log=True):
        '''
        using log_sem (for accreted multiple threads logging)
        :param log_level: which log level will log the msg
        :param msg: str
        :param if_log: if print to log or stdout
        :return:none
        '''
        if hasattr(self, 'log_sem'):
            time_s = datetime.datetime.now().strftime("%d.%m.%y-%H:%M")
            self.log_sem.acquire()
            if if_log:
                getattr(logging, log_level)("%s: %s" % (time_s, msg))
            else:
                print msg
            self.log_sem.release()

    def get_msg(self, who_from, sock):
        message = sock.recv(Helper.SOCK_SIZE)
        d = json.loads(message)
        self.log('debug', "got from %s: %s" % (who_from, d))
        return (d['cmd'], tuple(d['args']), d['msg'])

    def send_msg(self, who_to, sock, message):
        d = dict()
        d['msg'] = message
        message = message.split(' ')
        d['cmd'] = message[0]
        d['args'] = tuple(message[1:])
        self.log('debug', "send to %s: %s" % (who_to, d))
        sock.send(json.dumps(d))
