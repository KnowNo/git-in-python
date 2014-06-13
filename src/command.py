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
    def cmd_init(workspace, bare):
        Repository.create_repository(workspace, bare)

    @staticmethod
    def cmd_add(workspace, file):
        Repository(workspace).stage(file)

    @staticmethod
    def cmd_commit():
        pass

    @staticmethod
    def cmd_push():
        pass

    @staticmethod
    def cmd_clone():
        pass


