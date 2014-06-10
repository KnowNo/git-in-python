'''
Created on Jun 9, 2014

@author: lzrak47
'''

from repository import Repository


class Command(object):

    '''
    handle all commands
    '''

    @staticmethod
    def cmd_init(root, bare):
        repo = Repository(root, create=True, bare=bare)
        print repo

    @staticmethod
    def cmd_add():
        pass

    @staticmethod
    def cmd_commit():
        pass

    @staticmethod
    def cmd_push():
        pass

    @staticmethod
    def cmd_clone():
        pass


