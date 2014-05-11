#-------------------------------------------------------------------------------
# Name:        IService
# Purpose:     Used to manage services
#
# Author:      LoadLow
#
# Created:     11/05/2014
# Copyright:   (c) LoadLow 2014
#-------------------------------------------------------------------------------

class IService:

    def __init__(self):
        pass

    def start(self, config):
        pass

    def stop(self):
        pass

    def commit(self):
        pass
