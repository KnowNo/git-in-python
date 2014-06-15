'''
Created on Jun 9, 2014

@author: lzrak47
'''
import os

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
        if file == '.':
            file_list = []
            for root, dirs, files in os.walk('.'):
                if ".git" in dirs:
                    dirs.remove('.git')
                for file in files:
                    file_list.append(os.path.join(root[2:], file))
            Repository(workspace).stage(file_list)
        else:
            Repository(workspace).stage([file])

    @staticmethod
    def cmd_commit(workspace, msg):
        Repository(workspace).commit(msg)

    @staticmethod
    def cmd_push():
        pass

    @staticmethod
    def cmd_clone():
        pass


