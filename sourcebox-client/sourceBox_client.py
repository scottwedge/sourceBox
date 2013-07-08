# -*- coding: utf-8 -*-#

# imports
import os
import logging
import filesystem_controller
import client_communication_controller
import config_parser
import sourcebox_gui


class ClientBox(object):

    """description of class"""

    # Creates a new instance of the ClientTest
    def __init__(self):
        # delete old log file
        if os.path.exists("client.log"):
            os.remove("client.log")

        # create logger
        self.setupLogging("client", logging.DEBUG)
                          # replace DEBUG by INFO for less output

        self.log.debug('Starting Client...')
        try:
            self.gui = sourcebox_gui.SourceBox_Gui(self)
        # unexpected exit
        except KeyboardInterrupt:
            del self.comm
            del self.fs

    def __del__(self):
        pass

    def start(self, gui):
        try:
            self.log.debug("Reading Config File...")
            config = config_parser.Config_Parser('./sb_client.conf')

            self.log.debug("Creating GUI...")
            self.gui = gui

            self.log.debug("Creating Filesystem Controller...")
            self.fs = filesystem_controller.Filesystem_Controller(
                self, config.boxPath)

            self.log.debug("Creating Communication Controller...")
            self.comm = client_communication_controller.Client_Communication_Controller(
                self, config.serverIP, config.serverPort, config.clientName)

            self.log.info('Client is running')
        except Exception, e:
            gui.changeStatus()
            self.log.error(e)

    def stop(self):
        try:
            del self.comm
            del self.fs
        except:
            self.log.error(
                "Could not delete client objects. Maybe the were not created")

    # creates global log object
    # @param name the name of the logger
    # @param level level of logging e.g. logging.DEBUG
    # @author Emanuel Regnath
    def setupLogging(self, name, level):
        self.log = logging.getLogger(name)
        self.log.setLevel(level)

        formatter = logging.Formatter('[%(levelname)s] %(message)s')

        sh = logging.StreamHandler()
        sh.setLevel(level)
        sh.setFormatter(formatter)
        self.log.addHandler(sh)

        fh = logging.FileHandler(name + ".log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.log.addHandler(fh)
