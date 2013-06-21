import rcslib

## @package Data_Controller
# handles the communication with the backend
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Martin
#
class Data_Controller(object):

    data_dir = ''

    ## Creates a new instance of the data controller
    # @param data_dir The directory where the data is being stored
    #
    def __init__(self, data_dir):
        self.rcs = rcslib.RCS()
        print 'Created Data_Controller in dir ' + data_dir
    
    ##  Reads a file
    # @param file_name name of the file
    #
    def read_file(self, file_name):
        current_file = open(file_name, 'r')
        return current_file.read()

    ## Checks if a file is locked
    # @param file_name name of the file
    #
    def is_locked(self, file_name):
        return self.rcs.islocked(file_name)

    ## Locks a file
    # @param file_name name of the file
    #
    def lock_file(self, file_name):
        self.rcs.checkout(file_name, True)

    ## Unlocks a file
    # @param file_name name of the file
    #
    def unlock_file(self, file_name):
        self.rcs.unlock(file_name)

    ## Deletes a file
    # @param file_name name of the file
    #
    def delete_file(self, file_name):
        self.rcs._remove(file_name)

    ## Creates a new file
    # @param file_name name of the file
    #
    def create_file(self, file_name):
        print 'Create file ' + file_name
        self.rcs.checkin(file_name, 'Created file ' + file_name)

    ## Saves a file
    # @param file_name name of the file
    # @param content the content to be stored in the file
    #
    def save_file(self, file_name, content):
        current_file = open(file_name, 'w')
        current_file.write(content)
        self.rcs.checkin(file_name, 'Changed by user')

    ## Show changes of the file
    # @param file_name name of the file
    #
    def show_changes(self, file_name):
        return self.rcs.log(file_name)