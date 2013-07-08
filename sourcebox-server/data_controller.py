import rcslib
import os
import logging

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
        self.data_dir = './data'
        # catch logging object
        self.log = logging.getLogger("server")

        self.log.info('Created Data_Controller in dir ' + self.data_dir)

    # Reads a file
    # @param file_path name of the file
    #
    def read_file(self, file_path):
        path = os.path.join(self.data_dir, file_path)
        self.log.debug('reading file ' + path)
        with open(path, 'r') as open_file:
            content = open_file.read()
        return content

    # Checks if a file is locked
    # @param file_name name of the file
    #
    def is_locked(self, file_name):
        path = os.path.join(self.data_dir, file_name)
        return self.rcs.islocked(path)

    # Locks a file
    # @param file_name name of the file
    #
    def lock_file(self, file_name, user):
        path = os.path.join(self.data_dir, file_name)
        self.rcs.checkout(path, user, True)

    # Unlocks a file
    # @param file_name name of the file
    #
    def unlock_file(self, file_name, user):
        path = os.path.join(self.data_dir, file_name)
        self.rcs.checkin(path, user, 'Unlocked file ' + path)

    # Deletes a file
    # @param file_name name of the file
    #
    def delete_file(self, file_name, user):
        try:
            path = os.path.join(self.data_dir, file_name)
            self.rcs._remove(path)
            os.remove(path + ',v')
        except OSError:
            self.log.error(
                'It seems that the file to be deleted is already gone. This is BAD!')

    # Creates a new file
    # @param file_path name of the file
    # @param content the content
    def create_file(self, file_path, user, content=''):
        try:
            path = os.path.join(self.data_dir, file_path)
            new_file = open(path, 'w+')
            new_file.write(content)
            new_file.close
            self.rcs.checkin(path, user, 'Created file ' + path)
            # self.rcs.lock(path, user)
            return True
        except IOError, err:
            self.log.error('Could not create file!')
            self.log.error(str(err))

    # Saves a file
    # @param file_name name of the file
    # @param content the content to be stored in the file
    #
    def modify_file(self, file_name, content, user):
        path = os.path.join(self.data_dir, file_name)
        # self.rcs.checkout(path, True, user)
        current_file = open(path, 'w')
        current_file.write(content)
        current_file.close()
        # self.rcs.checkin(path, user, 'Changed by user')
        # self.rcs.lock(path, user)

    # Show changes of the file
    # @param file_name name of the file
    #
    def show_changes(self, file_name):
        path = os.path.join(self.data_dir, file_name)
        return self.rcs.log(path)

    def list_dir(self):
        return os.listdir(self.data_dir)

    def move_file(oldpath, name, newpath, user):
        # return true if successfully moved
        pass
