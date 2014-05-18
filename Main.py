import sys, threading, serial, time, random, signal, atexit, Globals, struct, Constants
from App import App, AppHandler
from RemoteClientService import RemoteClientService
from SQLiteReposService import SQLiteReposService
from GeigerCOMService import GeigerCOMService
from HitEntity import HitEntity
from HitArrayEntity import HitArrayEntity
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
        print(error)
        pass

    def stop_error(self, service, error):
        print(error)
        pass

    def transact_error(self, service, error):
        print(error)
        pass

    def commit_error(self, service, error):
        print(error)
        pass

    def init_error(self, error):
        print(error)
        pass

def sigint_handler(signum, frame):
    print()
    print('Stopping Application...')
    Globals.Application.stop()
    time.sleep(5)
    exit(0)

signal.signal(signal.SIGINT, sigint_handler)

def main():
    print("ISN Geiger Project - Client")
    print("===========================")

    print("Starting application...")

    services = [SQLiteReposService(), GeigerCOMService(), RemoteClientService()]
    Globals.Application = App(AppHandlerImpl(), services)
    success = Globals.Application.start()

    if(success):
        print("Application started!")

        print()
        print('Type CTRL+C to stop the application')
        try:
            while True:
                time.sleep(1)
        except:
            pass
    else:
        print("Application not started!")
        print("exiting...")
        time.sleep(10)
        exit(0)
    pass

@atexit.register
def onExit():
    print("Application stopped!")


if __name__ == '__main__':
    main()