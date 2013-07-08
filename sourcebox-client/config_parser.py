# -*- coding: utf-8 -*-#
import ConfigParser

## --------------------------------------------------------------
## PARSE CONFIG FILE
## --------------------------------------------------------------

class Config_Parser(object):

	## Constructor
	def __init__(self, config_file):
		self.configfile = config_file
		self.config = ConfigParser.ConfigParser()
		self.config.read(self.configfile)
		#try:
		#	config.read(config_file)
		#except:
		#	print "Error while trying to read config file. Check if 'sb_client.conf' exists in the same folder as the program file."

		self.boxPath = self.config.get('main', 'path')
		self.clientName = self.config.get('main', 'name')

		self.serverHostname = self.config.get('server', 'host')
		self.serverIP = self.config.get('server', 'ip')
		self.serverPort = self.config.get('server', 'port')

	def writeConfig(self, path, ip):
		self.config.set('main', 'path', path)
		self.config.set('server', 'ip', ip)
		with open(self.configfile, 'wb') as configfile:
			self.config.write(configfile)