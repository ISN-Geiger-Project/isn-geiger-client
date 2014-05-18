import sys, threading, asyncore, Constants
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
            else: self.configPath = Constants.DEFAULT_CONFIG_PATH
            self.running = False
            self.services = services
            self.config = RawConfigParser()
            self.config.readfp(open(self.configPath))

            self.mainConfig = SubConfiguration(self.config, "Main")
            self.commitTimer = threading.Timer(self.mainConfig.getint("commit_interval"), self.__commitServices)
            self.commitTimer.setDaemon(True)
            self.asyncLoop = threading.Thread(target = self.__loopAsync)
            self.asyncLoop.setDaemon(True)
        except Exception as e:
            self.handler.init_error(e)

     def __loopAsync(self):
        asyncore.loop()

     def __commitServices(self):
        for service in self.services:
            try:
                service.commit()
            except Exception as e:
                self.handler.commit_error(service, e)
                pass

     def start(self):
        if not self.running:
            self.running = True
            for service in self.services:
                try:
                    service.start(SubConfiguration(self.config, service.__class__.__name__))
                except Exception as e:
                    self.handler.start_error(service, e)
                    return False
            self.asyncLoop.start()
            self.commitTimer.start();
            return True

     def stop(self):
        if self.running:
            self.running = False
            self.commitTimer.cancel()
            for service in self.services:
                try:
                    service.stop()
                except Exception as e:
                    self.handler.stop_error(service, e)
                    pass
            asyncore.close_all()
            self.asyncLoop.join()

     def exit(self):
        print()
        print('Stopping Application...')
        self.stop()
        time.sleep(5)
        exit(0)

     def transact(self, entity):
        for service in self.services:
            try:
                entity.serialize(service)
            except Exception as e:
                self.handler.transact_error(service, e)
                pass

     def receive(self, data, klass):
        return klass().deserialize(service, data)

     def get(self, serviceClass):
        for service in self.services:
            if(service.__class__ == serviceClass): return service
        return None


class AppHandler:
    def __init__(self):
        pass

    def start_error(self, service, error):

        pass

    def stop_error(self, service, error):
        pass

    def transact_error(self, service, error):
        pass

    def commit_error(self, service, error):
        pass

    def init_error(self, error):
        pass

pass