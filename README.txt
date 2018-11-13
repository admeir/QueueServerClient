#README

run first: 
./QueueServer.py --ip IP --port PORT 
then from another terminal:
./Client.py --ip IP --port PORT 

sever/client API:
Server answering on all valid API
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


usage: QueueServer.py [-h] --ip IP --port PORT [--log_level LOG_LEVEL]

optional arguments:
  -h, --help            show this help message and exit
  --ip IP               SERVER IP ADDRESS
  --port PORT           SERVER PORT
  --log_level LOG_LEVEL
                        loging levels: INFO, DEBUG

usage: Client.py [-h] --ip IP --port PORT [--log_level LOG_LEVEL]

optional arguments:
  -h, --help            show this help message and exit
  --ip IP               SERVER IP ADDRESS
  --port PORT           SERVER PORT
  --log_level LOG_LEVEL
                        loging levels: INFO, DEBUG




