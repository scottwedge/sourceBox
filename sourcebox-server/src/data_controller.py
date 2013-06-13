#
# Data_Controller
# handles the communication with the backend
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Martin
#

import subprocess
import os.path

class Data_Controller(object):

    data_dir = ''
    def __init__(self, data_dir):
        Data_Controller.data_dir = os.path.abspath(data_dir)
        print 'Created Data_Controller in dir ' + data_dir

    def lock_file(self, file_name):
        arguments = ['co', '-l', file_name]
        process = subprocess.Popen(arguments)
        process.wait()

    def unlock_file(self):
        pass

    def delete_file(self):
        pass

    def create_file(self, file_name):
        print 'Create file ' + file_name
        arguments = ['ci', '-u', '-m\'Auto Checkin.\'', file_name]
        process = subprocess.Popen(arguments)
        process.wait()


    def save_file():
        pass
