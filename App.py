import sys
from configparser import ConfigParser, RawConfigParser

from SubConfiguration import SubConfiguration

#-------------------------------------------------------------------------------
# Name:        App
# Purpose:     Main app class
#
# Author:      LoadLow
#
# Created:     11/05/2014
# Copyright:   (c) LoadLow 2014
#-------------------------------------------------------------------------------

class App:
     def __init__(self, handler, services):
        self.handler = handler
        try:
            if(sys.argv.__len__() > 1): self.configPath = sys.argv[1]
            else: self.configPath = "config.cfg"
            self.services = services
            self.config = RawConfigParser()
            self.config.readfp(open(self.configPath))
        except Exception as e:
            self.handler.init_error(e)
            pass

     def start(self):
        for service in self.services:
            try:
                service.start(SubConfiguration(self.config, service.__class__.__name__))
            except Exception as e:
                self.handler.start_error(service, e)
                pass

     def stop(self):
        for service in self.services:
            try:
                service.stop()
            except Exception as e:
                self.handler.stop_error(service, e)
                pass

     def transact(self, data):
        for service in self.services:
            try:
                data.serializeObject(service)
            except Exception as e:
                self.handler.transact_error(service, e)
                pass

class AppHandler:
    def __init__(self):
        pass

    def start_error(self, service, error):
        pass

    def stop_error(self, service, error):
        pass

    def transact_error(self, service, error):
        pass

    def init_error(self, error):
        pass

pass