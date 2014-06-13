'''
Created on Jun 9, 2014

@author: lzrak47
'''
import os

from config import Config
from objects import Blob
from utils import read_file, write_to_file


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
        
        
    def stage(self, file):
        try:
            content = read_file(file)
            blob = Blob(self.workspace, content)
            if not os.path.exists(blob.path):
                dir = os.path.dirname(blob.path)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                write_to_file(blob.path, blob.content)
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
            
        config = Config(init_config_dict)
        write_to_file('config', config.convert_dict_to_str())
                