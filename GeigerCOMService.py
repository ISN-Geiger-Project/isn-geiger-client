from IService import IService
from SerialPort import SerialPort
from SerialPort import SerialPortHandler
from HitEntity import HitEntity
import time
import Globals, Constants

#-------------------------------------------------------------------------------
# Name:         GeigerCOMService
# Purpose:      Communication service between the Geiger counter and the serial
#               port
#
# Author:      LoadLow
#
# Created:     11/05/2014
# Copyright:   (c) LoadLow 2014
#-------------------------------------------------------------------------------
global Application

class GeigerCOMService(IService, SerialPortHandler):
    def __init__(self):
        self.serialPort = None
        pass

    def start(self, config):
        self.serialPort = SerialPort(self, config.get('port_address'), Constants.SERIAL_MESSAGE_DELIMITER)
        self.serialPort.openPort()
        pass

    def stop(self):
        if(self.serialPort != None):
            self.serialPort.abortPort()
        pass

    def commit(self):
        pass

    def port_opened(self, SerialPort):
        """When the port is opened."""
        print("Port linked!")
        pass

    def port_read(self, SerialPort, Data):
        """When str data has been recvd."""
        #Data starting by "N =" characters
        if(Data.startswith(Constants.SERIAL_MESSAGE_HEAD)):
            hitsCount = int(Data[Constants.SERIAL_MESSAGE_HEAD:])
            hits = HitEntity().set(int(time.time()), hitsCount)
            Globals.Application.transact(hits)
        pass

    def port_closed(self, SerialPort):
        """When the port is closed."""
        print("Port closed")
        self.serialPort.openPort()
        pass

    def port_error(self, SerialPort, Error):
        """When error has been encountered."""
        pass

    def port_abort(self, SerialPort):
        """When the port has been aborted."""
        print("Port aborted")
        pass
