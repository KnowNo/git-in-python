'''
Created on Jun 13, 2014

@author: lzrak47
'''

import os
import zlib

from utils import calSha1


class BaseObject(object):
    '''
    git base object
    '''


    def __init__(self, workspace, content):
        '''
        Constructor
        '''
        self.content = zlib.compress(content)
        self.sha1 = calSha1(content)
        self.path = os.path.join(workspace, '.git', 'objects', self.sha1[:2], self.sha1[2:])

class Blob(BaseObject):
    
    def __init__(self, workspace, content):
        real_content = 'blob %d\0%s' % (len(content), content)  
        super(Blob, self).__init__(workspace, real_content)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        