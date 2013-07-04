import rcslib
import os

# @package Data_Controller
# handles the communication with the backend
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Martin
#


class Data_Controller(object):

    # Creates a new instance of the data controller
    # @param data_dir The directory where the data is being stored
    #
    def __init__(self, data_dir):
        self.rcs = rcslib.RCS()
        self.data_dir = os.path.join('.', 'data')

        print '[INFO] Created Data_Controller in dir ' + self.data_dir

    # Reads a file
    # @param file_name name of the file
    #
    def read_file(self, file_name):
        current_file = open(file_name, 'r')
        return current_file.read()

    # Checks if a file is locked
    # @param file_name name of the file
    #
    def is_locked(self, file_name):
        path = os.path.join(self.data_dir, file_name)
        return self.rcs.islocked(path)

    # Locks a file
    # @param file_name name of the file
    #
    def lock_file(self, file_name):
        path = os.path.join(self.data_dir, file_name)
        self.rcs.lock(path)

    # Unlocks a file
    # @param file_name name of the file
    #
    def unlock_file(self, file_name):
        path = os.path.join(self.data_dir, file_name)
        self.rcs.unlock(path)

    # Deletes a file
    # @param file_name name of the file
    #
    def delete_file(self, file_name):
        try:
            path = os.path.join(self.data_dir, file_name)
            self.rcs._remove(path)
            os.remove(path + ',v')
        except OSError:
            print '[ERROR] It seems that the file to be deleted is already gone. This is BAD!'

    # Creates a new file
    # @param file_name name of the file
    # @param content the content
    def create_file(self, file_name, content=''):
        try:
            path = os.path.join(self.data_dir, file_name)
            new_file = open(path, 'w+')
            new_file.write(content)
            new_file.close
            self.rcs.checkin(path, 'Created file ' + path)
            self.rcs.lock(path)
            return True
        except IOError:
            print '[ERROR] Could not create file!'

    # Saves a file
    # @param file_name name of the file
    # @param content the content to be stored in the file
    #
    def modify_file(self, file_name, content):
        path = os.path.join(self.data_dir, file_name)
        self.rcs.checkout(path, True)
        current_file = open(path, 'w')
        current_file.write(content)
        current_file.close()
        self.rcs.checkin(path, 'Changed by user')
        self.rcs.lock(path)

    # Show changes of the file
    # @param file_name name of the file
    #
    def show_changes(self, file_name):
        path = os.path.join(self.data_dir, file_name)
        return self.rcs.log(path)

    def move_file(oldpath, name, newpath):
        # return true if successfully moved
        pass
