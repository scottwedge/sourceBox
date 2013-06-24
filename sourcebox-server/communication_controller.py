#
# Communication_Controller
# handles the communication with the clients
#
# @encode  UTF-8, tabwidth = , newline = LF
# @author  Paul
#


# push functions (requests)


class Communication_Controller(object):

    def __init__(self, parent):
        print 'Created Communication_Controller'
        parent.data.lock_file('./data/test.txt')

    def update_files(self):
        pass

    # pull functions (response)
    def create_file(self):
        pass

    def lock_file(self):
        pass

    def modify_file(self):
        pass

    def unlock_file(self):
        pass

    def delete_file(self):
        pass

    # Internal functions
    def _create_socket(self):
        pass
