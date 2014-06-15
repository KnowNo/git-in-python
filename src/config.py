'''
Created on Jun 9, 2014

@author: lzrak47
'''

import os
from utils import read_file

class Config(object):
    '''
    config file
    '''


    def __init__(self, workspace):
        '''
        Constructor
        '''
        self.workspace = workspace
        self.config_dict = {}
        paths = ['/etc/config', os.path.expanduser('~') + '/.gitconfig', os.path.join(workspace, '.git', 'config')]
        for path in paths:
            if os.path.exists(path):
                self._parse_config_to_dict(path)
    
    
    def _parse_config_to_dict(self, path):
        content = read_file(path)
        for entry in content.split('[')[1:]:
            index_key_val = entry.split(']')
            index = index_key_val[0]
            key_val_list = index_key_val[1]
            self.config_dict[index] = self.config_dict.get(index, {})
            for key_val in key_val_list.split('\n\t')[1:]:
                key = key_val.split(' = ')[0].strip()
                val = key_val.split(' = ')[1].strip()
                self.config_dict[index][key] = val
             
    
    @staticmethod
    def create_config(config_dict):
        str = ''
        for index, key_value in config_dict.iteritems():
            str += '[%s]\n' % (index)
            for key, value in key_value.iteritems():
                str +='\t%s = %s\n' % (key, value)
        return str
        
    
            
            
        
    
    
    
        