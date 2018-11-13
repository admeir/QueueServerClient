#!/usr/bin/python
from Helper import Helper
from Server import Server
from MyQueue import MyQueue

cmd_help_txt = '''
    API:
        ENQ <Item>
            Returns status OK or message if there is an error
        DEQ
            Returns the item or message is there is an error
        STAT
            Returns the number of items in the stack
        STOP
            Stops the server
        DEBUG <on|off>
            Enable / Disable log messages in the server
'''


class QueueServer(Server):
    def __init__(self):
        Helper.LOGGER_NAEM = 'QueueServer'
        super(QueueServer, self).__init__()
        self.queue = MyQueue()

    def server_up(self):
        super(QueueServer, self).server_up()
        self.menage_clients(self.api)

    def api(self, client_ip, client_con):
        '''
            answering on all valid API
                ENQ <Item>
                    Returns status OK or message if there is an error
                DEQ
                    Returns the item or message is there is an error
                STAT
                    Returns the number of items in the stack
                STOP
                    Stops the server
                DEBUG <on|off>
                    Enable / Disable log messages in the server
        '''
        while self.connection_up:
            try:
                cmd, args, _ = self.get_msg(client_ip, client_con)
                if len(cmd):
                    # 'ENQ' and <ITEM> to enqueue to queue
                    if cmd == 'ENQ':
                        self.send_msg(client_ip, client_con,
                                      self.queue.enq(*args))
                    elif cmd == 'DEQ':
                        self.send_msg(client_ip, client_con,
                                      self.queue.deq())
                    elif cmd == 'STAT':
                        self.send_msg(client_ip, client_con,
                                      self.queue.status())
                    elif cmd == 'STOP':
                        self.broadcast_message("STOP")
                        self.server_down()
                    elif cmd == 'DEBUG':# DEBUG <ON/OFF>
                        self.send_msg(client_ip, client_con,
                                      self.change_log_level(*args))
                    else:
                        self.send_msg(client_ip, client_con,
                                      "<ERROR:INVALID-COMMAND!>%s" % cmd_help_txt)
            except Exception:
                pass

    def change_log_level(self, log_on_off):
        if log_on_off == 'ON':
            super(QueueServer, self).change_log_level('DEBUG')
            self.log('debug', "DEBUG MODE-%s" % (log_on_off))
        elif log_on_off == 'OFF':
            self.log('debug', "DEBUG MODE-%s" % (log_on_off))
            super(QueueServer, self).change_log_level('INFO')
        else:
            return "BAD-INPUT"
        return '<OK>'

if __name__ == '__main__':
    server = QueueServer()
    server.server_up()
