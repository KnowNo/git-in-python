'''
Created on Jun 9, 2014

@author: lzrak47
'''
import os

from termcolor import colored

from branch import Branch
from constants import GIT_DIR
from repository import Repository
from utils import get_all_files_in_dir, filter_by_gitignore


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
            Repository().stage(filter_by_gitignore(get_all_files_in_dir('.', GIT_DIR)))
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
    def cmd_branch(name, is_deleted):
        b = Branch()
        if not name:
            for branch in b.get_all_branches():
                print '* %s' % colored(branch, 'green') if branch == b.head_name else '  %s' % branch
        elif is_deleted:
            b.delete_branch(name)
        else :
            b.add_branch(name)
    
    @staticmethod
    def cmd_reset(commit_sha1, is_soft, is_hard):
        repo = Repository()
        pre_entries = dict(repo.index.entries)  
        repo.update_head_commit(commit_sha1)
        if not is_soft:
            repo.rebuild_index_from_commit(commit_sha1)
            if is_hard:
                repo.rebuild_working_tree(pre_entries)
    
    @staticmethod
    def cmd_checkout(branch):
        b = Branch()
        b.switch_branch(branch)
        repo = Repository()
        pre_entries = dict(repo.index.entries)  
        repo.rebuild_index_from_commit(repo.branch.head_commit)
        repo.rebuild_working_tree(pre_entries)
    
    @staticmethod
    def cmd_push():
        pass

    @staticmethod
    def cmd_clone():
        pass


