#
# sourceboxclient – Filesystem_Controller
# handles the communication with filesystem
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Emu
#


# watchdog 0.6: alle plattformen, leider nur modified, create und delete
# pyinotify: nur Linux, allerdings mit open event






## --------------------------------------------------------------
## PARSE CONFIG FILE
## --------------------------------------------------------------
config = ConfigParser.ConfigParser()
try:
    config.read("./sb_client.conf")
except:
	print "Error while trying to read config file. Check if 'sb_client.conf' exists in the same folder as the program file."

boxPath = config.get('main', 'path')




class Filesystem_Controller(object):

    def __init__(self):
        print 'Created Communication_Controller'

        def checkFiles(self, path):
            pass

        def lockFile(self, file):
            print "File " + file + " locked!"

        def updateFile(self, file):
            pass
