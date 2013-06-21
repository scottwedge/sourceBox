#
# Data_Controller
# handles the communication with the backend
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Martin
#
import rcslib

class Data_Controller(object):

    data_dir = ''
    def __init__(self, data_dir):
        self.rcs = rcslib.RCS()
        print 'Created Data_Controller in dir ' + data_dir
    def read_file(self, file_name):
        current_file = open(file_name, 'r')
        return current_file.read()

    def lock_file(self, file_name):
        self.rcs.checkout(file_name, True)

    def unlock_file(self, file_name):
        self.rcs.unlock(file_name)

    def delete_file(self, file_name):
        self.rcs._remove(file_name)

    def create_file(self, file_name):
        print 'Create file ' + file_name
        self.rcs.checkin(file_name, 'Created file ' + file_name)

    def save_file(self, file_name, content):
        current_file = open(file_name, 'w')
        current_file.write(content)
        self.rcs.checkin(file_name, 'Changed by user')

    def show_changes(self, file_name):
        return self.rcs.log(file_name)