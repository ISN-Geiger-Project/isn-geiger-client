from IService import IService
import sqlite3
import datetime

#-------------------------------------------------------------------------------
# Name:        SQLiteReposService
# Purpose:     Data storage service using SQLite
#
# Author:      LoadLow
#
# Created:     11/05/2014
# Copyright:   (c) LoadLow 2014
#-------------------------------------------------------------------------------

class SQLiteReposService(IService):
    def __init__(self):
        self.dbConn = None
        pass

    def start(self, config):
        self.dbConn = sqlite3.connect(config.get('db_file_path'), check_same_thread=False)

        currentDate = datetime.datetime.now()
        self.tableMonth = str(currentDate.year)+"_"+str(currentDate.month)
        self.newCursor().execute('CREATE TABLE IF NOT EXISTS "hits_'+self.tableMonth+'" ("timestamp"  INTEGER NOT NULL,"count"  INTEGER NOT NULL,PRIMARY KEY ("timestamp" ASC));')
        self.commit()
        pass

    def stop(self):
        if(self.dbConn != None):
            self.dbConn.commit()
            self.dbConn.close()
        pass

    def commit(self):
        if(self.dbConn != None):
            self.dbConn.commit()
        pass

    def getTableName(self):
        return "hits_"+self.tableMonth

    def newCursor(self):
        currentDate = datetime.datetime.now()
        nowMonth =  str(currentDate.year)+"_"+str(currentDate.month)
        if(self.tableMonth != nowMonth):
            self.tableMonth = nowMonth
            self.newCursor().execute('CREATE TABLE IF NOT EXISTS "hits_'+self.tableMonth+'" ("timestamp"  INTEGER NOT NULL,"count"  INTEGER NOT NULL,PRIMARY KEY ("timestamp" ASC));')
            self.commit()
        return self.dbConn.cursor()