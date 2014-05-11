import sys, threading, serial, time
from App import App, AppHandler

#-------------------------------------------------------------------------------
# Name:        Main
# Purpose:     Main class running this project
#
# Author:      LoadLow
#
# Created:     18/02/2014
# Copyright:   (c) LoadLow 2014
#-------------------------------------------------------------------------------

class AppHandlerImpl(AppHandler):
    def __init__(self):
        pass

    def start_error(self, service, error):
        pass

    def stop_error(self, service, error):
        pass

    def transact_error(self, service, error):
        pass

    def init_error(self, error):
        print(error)
        pass


global Application

def main():
    services = []
    global Application
    Application = App(AppHandlerImpl(), services)
    Application.start()
    pass

if __name__ == '__main__':
    main()