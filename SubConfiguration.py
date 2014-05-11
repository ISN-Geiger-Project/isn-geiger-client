#-------------------------------------------------------------------------------
# Name:        SubConfiguration
# Purpose:     Return a subconfiguration getting automatically options
#              written on the same section.
#
# Author:      LoadLow
#
# Created:     11/05/2014
# Copyright:   (c) LoadLow 2014
#-------------------------------------------------------------------------------
class SubConfiguration:
    def __init__(self, mainConfig, section):
        self.mainConfig = mainConfig
        self.section = section
        pass

    def get(self, option):
        return self.mainConfig.get(self.section, option)

    def getint(self, option):
        return self.mainConfig.getint(self.section, option)

    def getboolean(self, option):
        return self.mainConfig.getboolean(self.section, option)

    def getfloat(self, option):
        return self.mainConfig.getfloat(self.section, option)
