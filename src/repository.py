'''
Created on Jun 9, 2014

@author: lzrak47
'''
import os
import time

from config import Config
from index import Index
from objects import Blob, Commit
from utils import read_file, write_to_file, cal_mode, write_object_to_file


class Repository(object):
    '''
    The git repository
    '''

    GIT_DIR = '.git'
    
    INIT_DIR = [
        'branches',
        'hooks',
        'info',
        'objects',
        'objects/info',
        'objects/pack',
        'refs',
        'refs/heads',
        'refs/tags',
    ]
    
    INIT_FILE = [
        ['HEAD', 'ref: refs/heads/master'],
        ['description', 'Unnamed repository'],
        ['info/exclude', ''],
    ]
    
    
    def __init__(self, workspace):
        self.workspace = workspace
        self.index = Index(os.path.join(workspace, '.git', 'index'))
        self.config = Config(workspace)
        
    def stage(self, files):
        try:
            for file in files:
                content = read_file(file)
                blob = Blob(self.workspace, content)
                if not os.path.exists(blob.path):
                    write_object_to_file(blob.path, blob.content)
                stat = os.stat(os.path.join(self.workspace, file))
                self.index.add_entry(file, ctime=stat.st_ctime, mtime=stat.st_mtime, dev=stat.st_dev, ino=stat.st_ino, mode=cal_mode(stat.st_mode), \
                       uid=stat.st_uid, gid=stat.st_gid, size=stat.st_size,sha1=blob.sha1, flags=0)
            self.index.write_to_file()
                    
        except Exception, e:
            print 'stage file %s error: %s' % (file, e)
    
    @staticmethod   
    def create_repository(workspace, bare=False):
        if not os.path.exists(workspace): 
            os.mkdir(workspace)
        os.chdir(workspace)
                
        if not bare:
            os.mkdir(Repository.GIT_DIR)
            os.chdir(Repository.GIT_DIR)
                
        for new_dir in Repository.INIT_DIR:
            os.mkdir(new_dir)
                
        for file_and_content in Repository.INIT_FILE:
            file_name = file_and_content[0]  
            content = file_and_content[1]
            write_to_file(file_name, content)
            
            
        init_config_dict = {
            'core': {
                'repositoryformatversion' : '0',
                'filemode' : 'true',
                'bare' : str(bare).lower(),
                'logallrefupdates' : 'true',
            }
        }
            
        content = Config.create_config(init_config_dict)
        write_to_file('config', content)
    
    def commit(self, msg, ref='HEAD'):
        cur_tree = self.index.do_commit(self.workspace)
        branch_name = read_file(os.path.join(self.workspace, '.git', 'HEAD')).strip('\n').rsplit('/', 1)[-1]
        ref_path = os.path.join(self.workspace, '.git', 'refs', 'heads', branch_name)
        parent_sha1 = None
        if os.path.exists(ref_path):
            parent_sha1 = read_file(ref_path) 
        committer_name = self.config.config_dict['user']['name']
        committer_email = '<%s>' %  (self.config.config_dict['user']['email'])
        commit_time = int(time.time())
        
        #TO FIX
        commit_timezone = time.strftime("%z", time.gmtime())
        
        commit = Commit(self.workspace, tree_sha1=cur_tree.sha1, parent_sha1=parent_sha1, name=committer_name, email=committer_email, \
                        timestamp=commit_time, timezone=commit_timezone, msg=msg)
        write_object_to_file(commit.path, commit.content)
        write_to_file(ref_path, commit.sha1)
        
    def delete(self, file):
        del self.index.entries[file]
        self.index.write_to_file()
        