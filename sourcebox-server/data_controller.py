import rcslib
import os
import logging
import shutil

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
    # @param file_path name of the file
    #
    def is_locked(self, file_path):
        path = os.path.join(self.data_dir, file_path)
        return self.rcs.islocked(path)

    # Locks a file
    # @param file_path name of the file
    #
    def lock_file(self, file_path, user):
        path = os.path.join(self.data_dir, file_path)
        try:
            self.rcs.checkout(path, user, True)
            return True
        except (OSError, IOError), err:
            self.log.error('Could not lock file because ' + str(err))
            return False

    # Unlocks a file
    # @param file_path name of the file
    #
    def unlock_file(self, file_path, user):
        path = os.path.join(self.data_dir, file_path)
        try:
            self.rcs.checkin(path, user, 'Unlocked file ' + path)
            return True
        except IOError, err:
            self.log.error('Could not unlock file because ' + str(err))
            return False

    # Deletes a file
    # @param file_path path relative to the sourceBox
    #
    def delete_file(self, file_path, user):
        try:
            path = os.path.join(self.data_dir, file_path)
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
            return False

    # Saves a file
    # @param file_name name of the file
    # @param content the content to be stored in the file
    #
    def modify_file(self, file_name, content, user):
        path = os.path.join(self.data_dir, file_name)
        try:
            with open(path, 'w') as current_file:
                current_file.write(content)
            return True
        except IOError, err:
            self.log.error('Could not modify file because ' + str(err))
            return False

    # Show changes of the file
    # @param file_path name of the file
    #
    def show_changes(self, file_path):
        path = os.path.join(self.data_dir, file_path)
        return self.rcs.log(path)

    def list_dir(self):
        return os.listdir(self.data_dir)

    def move_file(self, oldpath, name, newpath, user):
        # return true if successfully moved
        pass

    # creates a dir
    # @param path path relative to the sourceBox root
    def create_dir(self, path):
        path = os.path.join(self.data_dir, path)
        try:
            os.makedirs(path)
        except OSError, err:
            self.log.error(str(err))
        return True

    # deletes a dir
    # @param path path relative to the sourceBox root
    def delete_dir(self, path):
        path = os.path.join(self.data_dir, path)
        try:
            shutil.rmtree(path)
        except OSError, err:
            self.log.error(str(err))
        return True

    def move(self, old_file_path, new_file_path):
        old_file_path = os.path.join(self.data_dir, old_file_path)
        new_file_path = os.path.join(self.data_dir, new_file_path)
        if os.path.isdir(old_file_path):
            try:
                shutil.move(old_file_path, new_file_path)
            except (OSError, IOError), err:
                self.log.error(str(err))
        else:
            try:
                shutil.move(old_file_path, new_file_path)
                shutil.move(old_file_path + ',v' , new_file_path + ',v' )
            except (OSError, IOError), err:
                self.log.error(str(err))

        return True

    # gets the size of a file
    # @param path the path relative to the source box root
    # @param file_name the file name
    def get_file_size(self, file_path):
        if os.path.exists(os.path.join(self.data_dir, file_path)):
            return os.path.getsize(os.path.join(self.data_dir, file_path))
        else:
            return False
