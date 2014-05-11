from IService import IService
from SerialPort import SerialPort
from SerialPort import SerialPortHandler

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

class GeigerCOMService(IService, SerialPortHandler):
    def __init__(self):
        self.serialPort = None
        pass

    def start(self, config):
        self.serialPort = SerialPort(self, config.get('port_address'), config.get('data_separator'))
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
        pass

    def port_read(self, SerialPort, Data):
        """When str data has been recvd."""
        pass

    def port_closed(self, SerialPort):
        """When the port is closed."""
        pass

    def port_error(self, SerialPort, Error):
        """When error has been encountered."""
        pass

    def port_abort(self, SerialPort):
        """When the port has been aborted."""
        pass
