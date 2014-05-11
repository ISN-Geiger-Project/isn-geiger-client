from IService import IService
import sqlite3

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
        self.dbConn = sqlite3.connect(config.get('db_file_path'))
        pass

    def stop(self):
        if(self.dbConn != None):
            self.dbConn.close()
        pass

    def commit(self):
        if(self.dbConn != None):
            self.dbConn.commit()
        pass

    def newCursor(self):
        return self.dbConn.cursor()
