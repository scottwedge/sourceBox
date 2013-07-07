# -*- coding: utf-8 -*-#

# imports
import logging
import filesystem_controller
import client_communication_controller
import config_parser
import sourcebox_gui


class ClientBox(object):

    """description of class"""

    # Creates a new instance of the ClientTest
    def __init__(self):

        # create logger
        self.setupLogging("client", logging.DEBUG)              # replace DEBUG by INFO for less output

        log.debug('Starting Client...')
        try:
            self.gui = sourcebox_gui.SourceBox_Gui(self)
        # unexpected exit
        except KeyboardInterrupt:
            del self.comm
            del self.fs

    def start(self, gui):
        try:
            log.debug("Reading Config File...")
            config = config_parser.Config_Parser('./sb_client.conf')

            log.debug("Creating GUI...")
            self.gui = gui

            log.debug("Creating Communication Controller...")
            self.comm = client_communication_controller.Client_Communication_Controller(
                self, '127.0.0.1', 50000, 'Test_Computer1')

            log.debug("Reading Config File...")
            self.fs = filesystem_controller.Filesystem_Controller(
                self, config.boxPath)

            log.info('Client is running')
        except Exception, e:
            gui.changeStatus()
            log.error(e)
            
    def stop(self):
        try:
            del self.comm
            del self.fs
        except:
            log.error("Could not delete client objects. Maybe the were not created")


    # creates global log object
    # @param name the name of the logger
    # @param level level of logging e.g. logging.DEBUG
    # @author Emanuel Regnath
    def setupLogging(self, name, level):
        global log
        log = logging.getLogger(name)
        log.setLevel(level)

        formatter = logging.Formatter('[%(levelname)s] %(message)s')

        sh = logging.StreamHandler()
        sh.setLevel(level)
        sh.setFormatter(formatter)
        log.addHandler(sh)

        fh = logging.FileHandler(name + ".log")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        log.addHandler(fh)
