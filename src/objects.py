'''
Created on Jun 13, 2014

@author: lzrak47
'''

import binascii
import os
import re
import zlib

from utils import cal_sha1, read_file


class BaseObject(object):
    '''
    git base object
    '''
    def __init__(self, workspace, final_content=None, sha1=None):
        '''
        Constructor
        '''
        if sha1:
            self.sha1 = sha1
            self.path = os.path.join(workspace, '.git', 'objects', self.sha1[:2], self.sha1[2:])
            self.content = read_file(self.path)
        else:
            self.content = zlib.compress(final_content)
            self.sha1 = cal_sha1(final_content)
            self.path = os.path.join(workspace, '.git', 'objects', self.sha1[:2], self.sha1[2:])

class Blob(BaseObject):
    
    def __init__(self, workspace, raw_content=None, sha1=None):
        final_content = 'blob %d\0%s' % (len(raw_content), raw_content)  
        super(Blob, self).__init__(workspace, final_content)

class Tree(BaseObject):
    def __init__(self, workspace, args=None, sha1=None):
        raw_content = ''
        for arg in args:
            raw_content += '%04o %s\0%s' % (arg['mode'], arg['name'], binascii.unhexlify(arg['sha1']))
        final_content = 'tree %d\0%s' % (len(raw_content), raw_content)
        super(Tree, self).__init__(workspace, final_content)


class Commit(BaseObject):
    def __init__(self, workspace, **kwargs):
        if kwargs['sha1']:
            super(Commit, self).__init__(workspace, sha1=kwargs['sha1'])
            final_content = zlib.decompress(self.content) 
            res = re.findall('parent (\w+)\n', final_content) 
            self.parent_sha1 = res[0] if res else None
            self.raw_content = final_content[final_content.find('tree'):]
            
        else:    
            raw_content = 'tree %s\n' % (kwargs['tree_sha1'])
            if kwargs['parent_sha1']:
                raw_content += 'parent %s\n' % (kwargs['parent_sha1'])
                
            raw_content += 'author %s %s %s %s\ncommitter %s %s %s %s\n\n%s\n' \
            % (kwargs['name'], kwargs['email'], kwargs['timestamp'], kwargs['timezone'] , \
                kwargs['name'], kwargs['email'], kwargs['timestamp'], kwargs['timezone'] , kwargs['msg'])
            
            final_content = 'commit %d\0%s' % (len(raw_content), raw_content)
            super(Commit, self).__init__(workspace, final_content)
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        