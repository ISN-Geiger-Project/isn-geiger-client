import hashlib, Constants, Globals, time, threading
from IService import IService
from NetConnector import NetConnector, NetConnectorHandler
from struct import *
from SQLiteReposService import SQLiteReposService
from HitArrayEntity import HitArrayEntity

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
        self.__registerPackets()
        self.lostPackets = list()
        self.alive = True
        pass

    def __reconnect(self):
        if self.alive:
            time.sleep(5)
            print('Testing reco...')
            del self.connector
            self.connector = NetConnector(self)
            self.connector.connectAsync(self.config.get('remote_host'), int(self.config.getint('remote_port')), self.config.getint('buffer_size'))
        pass

    def start(self, config):
        self.username = config.get('client_user')
        self.password = config.get('client_pass')
        self.config = config
        self.connector.connectAsync(config.get('remote_host'), int(config.getint('remote_port')), config.getint('buffer_size'))
        pass

    def __registerPackets(self):
        self.decoders = dict()
        self.decoders[Constants.PACKET_ASK_HITS_LIST] = self.__parse_AskHitsList
        self.decoders[Constants.PACKET_ASK_AUTH] = self.__parse_AskAuth
        self.decoders[Constants.PACKET_AUTH_SUCCESS] = self.__parse_AuthSuccess
        self.decoders[Constants.PACKET_AUTH_ERROR] = self.__parse_AuthError

    def stop(self):
        self.alive = False
        if self.connector != None:
            self.connector.close()
        pass

    def commit(self):
        pass

    def connection_opened(self):
        print('RemoteServer connection opened!')
        pass

    def packet_received(self, byteArray):
        byteArray = bytearray(byteArray)
        packetHeader = unpack(Constants.PACKET_HEADER_STRUCT, byteArray[:1])[0]
        if self.decoders.__contains__(packetHeader):
            packetDecoder = self.decoders[packetHeader]
            print('ReceivedPacket : '+ packetDecoder.__name__[8:])
            packetDecoder(byteArray[1:])
        pass

    def connection_closed(self):
        print('RemoteServer connection lost!')
        try: self.connector.close()
        except: pass
        self.__reconnect()
        pass

    def send(self, byteArray):
        if(self.connector.connected): self.connector.send(byteArray)
        else : self.lostPackets.append(byteArray)

    def __parse_AskHitsList(self, subData):
        start, end = unpack('!ii', subData)
        reposService = Globals.Application.get(SQLiteReposService)
        myQuery = 'SELECT * FROM hits_'+reposService.tableMonth + ' WHERE timestamp>='+str(start) + ' AND timestamp<='+str(end)
        cursor = reposService.newCursor().execute('SELECT * FROM hits_'+reposService.tableMonth + ' WHERE timestamp>='+str(start) + ' AND timestamp<='+str(end))
        hitsArray = HitArrayEntity().deserialize(cursor)
        hitsArray.serialize(self)
        pass

    def __parse_AskAuth(self, subData):
        length = unpack('!i', subData[:4])[0]
        keys = unpack('!'+str(length)+'i', subData[4:])
        dataKeys = ''
        for key in keys: dataKeys += str(key)

        digest = hashlib.md5((self.username+'\u0000'+self.password+'\u0000'+dataKeys).encode()).hexdigest()
        self.send(pack('!b'+str(digest.__len__())+'s', Constants.PACKET_RECV_AUTHKEY, digest.encode()))

    def __parse_AuthSuccess(self, subData):
        print("Authenticated on the server!")
        if self.lostPackets.__len__() > 0:
            for packet in self.lostPackets: self.send(packet)
            del self.lostPackets
            self.lostPackets = list()
            print("Lost packed synchronized!")
        pass

    def __parse_AuthError(self, subData):
        Globals.Application.exit()
        pass
