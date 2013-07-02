# -*- coding: utf-8 -*-#

# imports
from time import sleep
import filesystem_controller
import client_communication_controller
import config_parser
import sys


class ClientBox(object):
    """description of class"""

    # Creates a new instance of the ClientTest
    def __init__(self):
        print 'Starting Client...'
        try:
            # Parse config
            config = config_parser.Config_Parser('./sb_client.conf')

			# NOTE: Erstellen des comm controler schmeißt EX: AttributeError: "'Client_Communication_Controller' object has no attribute 'sock' 
            #self.comm = client_communication_controller.Client_Communication_Controller('127.0.0.1', 50000)
            self.fs = filesystem_controller.Filesystem_Controller(self, config.boxPath)
            print 'Client is running'    

        # unexpected exit
        except KeyboardInterrupt:
            print 'Fatal Error: Could not create Client'


	# main loop:
	try:
		while True:
			# receive lock command from server
			# wait for files system events
			sleep(1)
	# unexpected exit
	except KeyboardInterrupt:
		del self.comm
		del self.fs

