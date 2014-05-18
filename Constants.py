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