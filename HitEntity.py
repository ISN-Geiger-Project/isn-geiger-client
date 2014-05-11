from ISerializable import ISerializable
from SQLiteReposService import SQLiteReposService
from RemoteClientService import RemoteClientService
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
    def __init__(self, timestamp, count):
        self.timestamp = timestamp
        self.count = count

    def __init__(self):
        pass

    def serializeObject(self, target):
        if(target is SQLiteReposService):
            target.newCursor().executemany('INSERT INTO hits VALUES (?, ?)', [(self.timestamp, self.count)])
        elif(target is RemoteClientService):
            target.send(pack('bii', 0x01, self.timestamp, self.count))
        pass
