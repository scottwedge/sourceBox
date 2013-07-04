# -*- coding: utf-8 -*-#

# imports
import filesystem_controller
import client_communication_controller
import config_parser
import sourcebox_gui


class ClientBox(object):

    """description of class"""

    # Creates a new instance of the ClientTest
    def __init__(self):
        print 'Starting Client...'
        try:

            self.gui = sourcebox_gui.SourceBox_Gui(self)
        # unexpected exit
        except KeyboardInterrupt:
            del self.comm
            del self.fs

    def start(self, gui):
        try:
            config = config_parser.Config_Parser('./sb_client.conf')
            self.gui = gui
            self.comm = client_communication_controller.Client_Communication_Controller(
                self, '127.0.0.1', 50000, 'Test_Computer1')
            self.fs = filesystem_controller.Filesystem_Controller(
                self, config.boxPath)
            print 'Client is running'
        except:
            gui.changeStatus()

    def stop(self):
        try:
            del self.comm
            del self.fs
        except:
            print '[ERROR] Could not delete client objects. Maybe the were not created'
