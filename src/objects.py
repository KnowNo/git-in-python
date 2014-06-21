'''
Created on Jun 13, 2014

@author: lzrak47
'''

import binascii
import os
import re
import stat
import zlib

from constants import OBJECT_DIR
from utils import cal_sha1, read_file


class BaseObject(object):
    '''
    git base object
    '''
    def __init__(self, final_content=None, sha1=None):
        '''
        Constructor
        '''
        if sha1:
            self.sha1 = sha1
            self.path = os.path.join(OBJECT_DIR, self.sha1[:2], self.sha1[2:])
            self.content = read_file(self.path)
        else:
            self.content = zlib.compress(final_content)
            self.sha1 = cal_sha1(final_content)
            self.path = os.path.join(OBJECT_DIR, self.sha1[:2], self.sha1[2:])

class Blob(BaseObject):
    
    def __init__(self, raw_content=None, sha1=None):
        final_content = 'blob %d\0%s' % (len(raw_content), raw_content)  
        super(Blob, self).__init__(final_content)

class Tree(BaseObject):
    def __init__(self, args=None, sha1=None):
        if sha1:
            super(Tree, self).__init__(sha1=sha1)
            final_content = zlib.decompress(self.content) 
            self.raw_content = final_content[final_content.find('\0') + 1:]
            self.objects = re.findall('(\d+) (\S+)\0(.{20})', self.raw_content, re.S)
            
        else:
            raw_content = ''
            for arg in args:
                raw_content += '%04o %s\0%s' % (arg['mode'], arg['name'], binascii.unhexlify(arg['sha1']))
            final_content = 'tree %d\0%s' % (len(raw_content), raw_content)
            super(Tree, self).__init__(final_content)
            
    def parse_objects(self):
        res = {}
        queue = list(self.objects)
        while queue:
            object = queue.pop(0)
            mode, name, sha1 = object[0], object[1], binascii.hexlify(object[2])
            if stat.S_ISDIR(int(mode, 8)):
                new_objects = Tree(sha1=sha1).objects
                for new_object in new_objects:
                    queue.append([new_object[0], os.path.join(name, new_object[1]), new_object[2]])
            else:
                res[name] = {'mode' : mode, 'sha1' : sha1}
        return res


class Commit(BaseObject):
    def __init__(self, **kwargs):
        if kwargs['sha1']:
            super(Commit, self).__init__(sha1=kwargs['sha1'])
            final_content = zlib.decompress(self.content) 
            res = re.findall('parent (\w+)\n', final_content) 
            self.parent_sha1 = res[0] if res else None
            self.raw_content = final_content[final_content.find('tree'):]
            self.tree = re.findall('tree (\w+)\n', final_content)[0]
            
        else:    
            raw_content = 'tree %s\n' % (kwargs['tree_sha1'])
            if kwargs['parent_sha1']:
                raw_content += 'parent %s\n' % (kwargs['parent_sha1'])
                
            raw_content += 'author %s %s %s %s\ncommitter %s %s %s %s\n\n%s\n' \
            % (kwargs['name'], kwargs['email'], kwargs['timestamp'], kwargs['timezone'] , \
                kwargs['name'], kwargs['email'], kwargs['timestamp'], kwargs['timezone'] , kwargs['msg'])
            
            final_content = 'commit %d\0%s' % (len(raw_content), raw_content)
            super(Commit, self).__init__(final_content)
    
        