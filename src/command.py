'''
Created on Jun 9, 2014

@author: lzrak47
'''
import os

from constants import GIT_DIR
from repository import Repository
from utils import get_all_files_in_dir


class Command(object):

    '''
    handle all commands
    '''

    @staticmethod
    def cmd_init(workspace, bare):
        Repository.create_repository(workspace, bare)

    @staticmethod
    def cmd_add(file):
        if file == '.':
            Repository().stage(get_all_files_in_dir('.', GIT_DIR))
        else:
            Repository().stage([file])

    @staticmethod
    def cmd_rm(file, cached):
        Repository().delete(file)
        if not cached:
            os.remove(file)
        
    @staticmethod
    def cmd_commit(msg):
        Repository().commit(msg)

    @staticmethod
    def cmd_log(num):
        Repository().show_log(num)
    
    @staticmethod
    def cmd_status():
        Repository().show_status()
    
    @staticmethod
    def cmd_push():
        pass

    @staticmethod
    def cmd_clone():
        pass


