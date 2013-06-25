import ConfigParser

## --------------------------------------------------------------
## PARSE CONFIG FILE
## --------------------------------------------------------------

class Config_Parser(object):

	## Constructor
	def __init__(self, config_file):
		config = ConfigParser.ConfigParser()
		try:
			config.read(config_file)
		except:
			print "Error while trying to read config file. Check if 'sb_client.conf' exists in the same folder as the program file."

		self.boxPath = config.get('main', 'path')

		self.serverHostname = config.get('server', 'host')
		self.serverPort = config.get('server', 'port')

		self.username = config.get('user', 'name')
		self.password = config.get('user', 'password')