import asyncore
import socket
#-------------------------------------------------------------------------------
# Class Name:        NetConnector
# Purpose:           Used to communicate with an async socket managed by events
#
# Author:      LoadLow
#
# Created:     18/02/2014
# Copyright:   (c) LoadLow 2014
#-------------------------------------------------------------------------------
class NetConnector(asyncore.dispatcher_with_send):

    def __init__(self, aHandler):
        self.Handler = aHandler
        self.buffer_size = 1024
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        pass

    def connect(self, host, port, buffer_size=1024):
        self.buffer_size = buffer_size
        self.connect((host, port))
        pass

    def handle_connect(self):
        self.Handler.connection_opened()
        pass

    def handle_read(self):
        try:
            data = bytearray(self.recv(self.buffer_size))
            self.Handler.packet_received(data)
        except:
            pass

    def handle_close(self):
        self.Handler.connection_closed()
        self.close()
        pass
pass

class NetConnectorHandler:
    def __init__(self):
        pass

    def connection_opened(self):
        pass

    def packet_received(self, byteArray):
        pass

    def connection_closed(self):
        pass

pass