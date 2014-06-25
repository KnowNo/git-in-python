'''
Created on Jun 24, 2014

@author: lzrak47
'''
import os
import shutil

from constants import HEAD_PATH, REF_HEADS_DIR
from utils import read_file, write_to_file


class Branch(object):
    '''
    git branch 
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.head_name = read_file(HEAD_PATH).strip('\n').rsplit('/', 1)[-1]
        self.head_path = os.path.join(REF_HEADS_DIR, self.head_name)
        self.head_commit = read_file(self.head_path).strip() if os.path.exists(self.head_path) else None
    
    def get_all_branches(self):
        return os.listdir(REF_HEADS_DIR)
    
    def _check_branch_exists(self, name):
        return os.path.exists(os.path.join(REF_HEADS_DIR, name))
    
    def add_branch(self, name):
        if self._check_branch_exists(name):
            print "fatal: A branch named '%s' already exists." % (name)
            exit(1)
        shutil.copyfile(self.head_path, os.path.join(REF_HEADS_DIR, name))
    
    def delete_branch(self, name):
        if self.head_name == name:
            print "error: Cannot delete the branch '%s' which you are currently on." % (name)
            exit(1)
        os.remove(os.path.join(REF_HEADS_DIR, name))
    
    def switch_branch(self, name):
        if not self._check_branch_exists(name):
            print "error: branch '%s' did not match any branches known to git." % (name)
            exit(1)
        write_to_file(HEAD_PATH, 'ref: refs/heads/%s' % name)
            
        