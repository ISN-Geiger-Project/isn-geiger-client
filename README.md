isn-geiger-client
=================

>>ISN Geiger client receiving numeric data written in Python

>>NB : I'm using [PyScripter IDE](https://code.google.com/p/pyscripter/)

<h4>Structure :</h4>
![Structure](http://www.hostingpics.net/thumbs/84/88/36/mini_848836packages.png)
- backend: services writing/sending data
- frontend: services reading/receiving data
- serializable: objects that can be received or sent by communication services
- lib: classes used to create an application structure

<h4>Main.py is the main class, launching this app :</h4>
`````python
global Application

def main():
    #services instances
    services = []
    
    Globals.Application = App(AppHandlerImpl(), services)
    Globals.Application.start()
    pass

if __name__ == '__main__':
    main()
`````

<h4>Python execution :</h4>
`````bash
##default configFilePath = config.cfg
python Main.py [configFilePath]
`````

<h4>Configuration :</h4>
See "config.cfg" file

<h4>Constants :</h4>
constants are set on "Constants.py"
`````python
#Client Constants

#===========================PACKETS
PACKET_NULL = 0x00
#Packets sent by the client
PACKET_RECV_HIT = 0x01
PACKET_RECV_HITS_LIST = 0x02
PACKET_RECV_AUTHKEY = 0x03
#Packets sent by the server
PACKET_ASK_HITS_LIST = 0x04
PACKET_ASK_AUTH = 0x05
PACKET_AUTH_SUCCESS = 0x06
PACKET_AUTH_ERROR = 0x07

PACKET_HEADER_STRUCT = '!b'
DEFAULT_BUFFER_SIZE = 1024
#===========================PACKETS

#===========================APP
DEFAULT_CONFIG_PATH = "config.cfg"
#===========================APP

#===========================SERIAL PORT
SERIAL_PORT_BAUDRATE = 9600
SERIAL_MESSAGE_HEAD = "N = "
SERIAL_MESSAGE_DELIMITER = '\r\n'
#===========================SERIAL PORT
`````
