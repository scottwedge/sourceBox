# -*- coding: utf-8 -*-#
## sourceboxclient – main
#
# @encode  UTF-8, tabwidth = 4 , newline = LF
# @author  Gruppe4
#

# imports
from time import sleep
import filesystem_controller
import client_communication_controller
import config_parser

# Parse config
config = config_parser.Config_Parser('./sb_client.conf')

# Start Watchdog
filesystem_controller = filesystem_controller.Filesystem_Controller(config.boxPath)

# create communication_Controller
comm = client_communication_controller.Client_Communication_Controller('127.0.0.1', 50000)

# main loop:
try:

	while True:
		# receive lock command from server
		# wait for files system events
		sleep(1)
# unexpected exit
except KeyboardInterrupt:
	del filesystem_controller

