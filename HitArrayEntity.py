import Constants, sqlite3
from ISerializable import ISerializable
from struct import *
from HitEntity import HitEntity

#-------------------------------------------------------------------------------
# Name:        HitArrayEntity
# Purpose:     Represents an serializable array of hits objects
#
# Author:      LoadLow
#
# Created:     18/05/2014
# Copyright:   (c) LoadLow 2014
#------------------------------------------------------------------------------

class HitArrayEntity(ISerializable):
    def set(self, hitsArray):
        self.hitsArray = hitsArray
        return self

    def __init__(self):
        self.hitsArray = list()
        pass

    def serialize(self, target):
        from SQLiteReposService import SQLiteReposService
        from RemoteClientService import RemoteClientService
        if isinstance(target, SQLiteReposService):
            entities = []
            for entity in self.hitsArray:
                entities.append((entity.timestamp, entity.count))
            target.newCursor().executemany('INSERT INTO '+target.getTableName()+' VALUES (?, ?)', entities)
        elif isinstance(target, RemoteClientService):
            packet = bytearray()
            packet.extend(pack('!bi', Constants.PACKET_RECV_HITS_LIST, self.hitsArray.__len__()))
            for entity in self.hitsArray:
                packet.extend(pack('!ii', entity.timestamp, entity.count))
            target.send(packet)
        pass

    def deserialize(self, data):
        if isinstance(data, bytearray):
            length = unpack('!i', data[:4])[0]
            data = data[4:]
            for i in range(0, length):
                hit = HitEntity().deserialize(data[i*8:i*8+8])
                print(hit.timestamp, ' ; ', hit.count)
                self.hitsArray.append(hit)
            pass
        if isinstance(data, sqlite3.Cursor):
            hits = data.fetchall()
            if(hits.__len__() > 0):
                for hit in hits: self.hitsArray.append(HitEntity().set(hit[0], hit[1]))
            pass
        return self
