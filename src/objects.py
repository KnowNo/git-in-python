'''
Created on Jun 13, 2014

@author: lzrak47
'''

import binascii
import os
import zlib

from utils import cal_sha1


class BaseObject(object):
    '''
    git base object
    '''
    def __init__(self, workspace, content):
        '''
        Constructor
        '''
        self.content = zlib.compress(content)
        self.sha1 = cal_sha1(content)
        self.path = os.path.join(workspace, '.git', 'objects', self.sha1[:2], self.sha1[2:])

class Blob(BaseObject):
    
    def __init__(self, workspace, content):
        real_content = 'blob %d\0%s' % (len(content), content)  
        super(Blob, self).__init__(workspace, real_content)

class Tree(BaseObject):
    def __init__(self, workspace, args):
        content = ''
        for arg in args:
            content += '%04o %s\0%s' % (arg['mode'], arg['name'], binascii.unhexlify(arg['sha1']))
        real_content = 'tree %d\0%s' % (len(content), content)
        super(Tree, self).__init__(workspace, real_content)


class Commit(BaseObject):
    def __init__(self, workspace, **kwargs):
        content = 'tree %s\n' % (kwargs['tree_sha1'])
        if kwargs['parent_sha1']:
            content += 'parent %s\n' % (kwargs['parent_sha1'])
            
        content += 'author %s %s %s %s\ncommitter %s %s %s %s\n\n%s\n' \
        % (kwargs['name'], kwargs['email'], kwargs['timestamp'], kwargs['timezone'] , \
            kwargs['name'], kwargs['email'], kwargs['timestamp'], kwargs['timezone'] , kwargs['msg'])
        
        real_content = 'commit %d\0%s' % (len(content), content)
        super(Commit, self).__init__(workspace, real_content)
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        