import sys, threading, serial, time
from serial import *

#-------------------------------------------------------------------------------
# Name:        SerialPortManager
# Purpose:	   String communication on Serial Ports, managed in a parallel thread
#
# Author:      Loadlow
#
# Created:     18/02/2014
# Copyright:   (c) Loadlow 2014
#-------------------------------------------------------------------------------
class SerialPort(serial.Serial):

    def __task_inactive(self):
        """Inactive task (waiting an another task) : sleep 1 sec"""
        time.sleep(1.0)
        pass

    def __task_waiting_port(self):
        try:
            """Waiting the port connection."""
            self.open()
            if(self.isOpen()):
                try:
                    self.Handler.port_opened(self)
                except:
                    raise
                finally:
                    self.__CurrentTask = self.__task_reading_port
        except SerialException as e:
            """Port not found : sleep 2 secs"""
            try:
                self.Handler.port_error(self, e)
            except:
                raise
                pass
            time.sleep(2.0)
        pass

    def __task_reading_port(self):
        """Read port task. The reading timeout is set to "readingTimeout" (default value : 0.2)"""
        if not self.isOpen():
            try:
                self.Handler.port_closed(self)
            except:
                raise
            finally:
                self.__CurrentTask = self.__task_inactive
        else:
            try:
                currData = self.readline(eol = self.__DataDelimiter)
                if(currData):
                    self.Handler.port_read(self, currData.decode())
            except SerialTimeoutException:
                pass
        pass

    def __task_closing_port(self):
        """Async close port task."""
        self.close()
        if not self.isOpen():
            try:
                self.Handler.port_closed(self)
            except:
                raise
            finally:
                self.__CurrentTask = self.__task_inactive
        time.sleep(2.0)
        #Active = False
        pass

    def __init__(self, aHandler, aPort, aDataDelimiter = '\n', AutoFlush=True, readingTimeout = 0.2):
        """Create new inst of SerialPort """
        super().__init__()
        self.__CurrentTask = self.__task_inactive
        self.__Thread = None
        self.__sync = threading.RLock()
        self.__DataDelimiter = aDataDelimiter
        self.Active = False
        self.AutoFlush = AutoFlush

        self.Handler = aHandler
        self.port = aPort
        self.baudrate=9600
        self.parity=serial.PARITY_NONE
        self.stopbits=serial.STOPBITS_ONE
        self.bytesize=serial.EIGHTBITS
        self.timeout=readingTimeout
        pass

    def readline(self, size=None, eol=LF):
        """read a line which is terminated with end-of-line (eol) character
        ('\n' by default) or until timeout."""
        leneol = len(eol)
        line = bytearray()
        while True:
            c = self.read(1)
            if c:
                line += c
                if line[-leneol:] == eol:
                    break
                if size is not None and len(line) >= size:
                    break
            else:
                break
        return bytes(line)

    def openPort(self):
        """Set the thread task to Waiting Port if task is 'inactive'"""
        self.__sync.acquire()
        try:
            if self.__CurrentTask == self.__task_inactive:
                if not self.Active:
                        self.Active = True
                        self.__Thread = threading.Thread(None, self.__main_task, None)
                        self.__Thread.start()
                self.__CurrentTask = self.__task_waiting_port
        finally:
            self.__sync.release()
        pass

    def write(self, Data):
        """Write the given String Data on the serial port"""
        super().write((Data + self.__DataDelimiter).encode())
        if(self.AutoFlush):
            self.flushOutput()
        pass

    def closeAsync(self):
        """Close the port with the thread"""
        self.__sync.acquire()
        try:
            if(self.isOpen()):
                self.__CurrentTask = self.__task_closing_port
        finally:
            self.__sync.release()
        pass

    def abortPort(self):
        """Close the port and stop the thread."""
        self.__sync.acquire()
        try:
            self.Active = False
        finally:
            self.__sync.release()

    def __main_task(self):
        """Main thread running task."""
        while(self.Active):
            if not self.Active:
                break
            try:
                self.__sync.acquire()
                currTask = self.__CurrentTask
                self.__sync.release()
                currTask()
            except Exception as e:
                self.Handler.port_error(self, e)
            pass
        try:
            self.Handler.port_abort(self)
        except Exception as e:
            self.Handler.port_error(self, e)
        pass

pass

class SerialPortHandler:
    def __init__(self):
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

pass