import Constants
from ISerializable import ISerializable
from SQLiteReposService import SQLiteReposService
from struct import *

#-------------------------------------------------------------------------------
# Name:        HitEntity
# Purpose:     Represents an serializable hit object
#
# Author:      LoadLow
#
# Created:     11/05/2014
# Copyright:   (c) LoadLow 2014
#------------------------------------------------------------------------------

class HitEntity(ISerializable):
    def set(self, timestamp, count):
        self.timestamp = timestamp
        self.count = count
        return self

    def __init__(self):
        pass

    def serialize(self, target):
        if isinstance(target, SQLiteReposService):
            target.newCursor().executemany('INSERT INTO '+target.getTableName()+' VALUES (?, ?)', [(self.timestamp, self.count)])
        elif isinstance(target, RemoteClientService):
            target.send(pack('!bii', Constants.PACKET_RECV_HIT, self.timestamp, self.count))
        pass

    def deserialize(self, data):
        if isinstance(data, bytearray):
            self.timestamp, self.count = unpack('!ii', data)
##        elif isinstance(data, sqlite3.Row):
##
##            pass
##        elif isinstance(data, str):
##            if(str.startswith(Constants.SERIAL_MESSAGE_HEAD)):
##                self.timestamp = int(time.time())
##                self.count = int(Data[Constants.SERIAL_MESSAGE_HEAD:])
        return self
