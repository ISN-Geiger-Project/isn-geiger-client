from IService import IService
from NetConnector import NetConnector
from NetConnector import NetConnectorHandler
from struct import *

#-------------------------------------------------------------------------------
# Name:        RemoteClientService
# Purpose:     Communication service between the python client and the remote
#              server.
#
# Author:      LoadLow
#
# Created:     11/05/2014
# Copyright:   (c) LoadLow 2014
#-------------------------------------------------------------------------------

class RemoteClientService(IService, NetConnectorHandler):
    def __init__(self):
        self.connector = NetConnector(self)
        self.authKey = None
        pass

    def start(self, config):
        self.authKey = config.get('auth_key')
        self.connector.connect(config.get('remote_host'), config.getint('remote_address'), config.getint('buffer_size'))
        pass

    def stop(self):
        if(self.connector != None):
            self.connector.close()
        pass

    def commit(self):
        pass

    def connection_opened(self):
        self.send(pack('bs', 0x00, self.authKey))
        pass

    def packet_received(self, byteArray):
        pass

    def connection_closed(self):
        pass

    def send(self, byteArray):
        self.connector.send(byteArray)
        pass
