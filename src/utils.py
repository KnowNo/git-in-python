'''
Created on Jun 9, 2014

@author: lzrak47
'''

import hashlib
import os
import stat
import sys


S_IFGITLINK = 0o160000

def write_to_file(path, content):
    f = open(path, 'w')
    f.write(content)
    f.close()
    
def write_object_to_file(path, content):       
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.mkdir(dir)
    write_to_file(path, content)
    
def read_file(file_name):
    try:
        f = open(file_name, 'r')
        content = f.read()
        f.close()
        return content
    except Exception, e:
        print "open file %s error: %s" % (file_name, e)
        sys.exit(1)

def cal_sha1(content):
    sha1 = hashlib.sha1()
    sha1.update(content)
    return sha1.hexdigest()

def cal_mode(mode):
    if stat.S_ISLNK(mode):
        return stat.S_IFLNK
    elif stat.S_ISDIR(mode):
        return stat.S_IFDIR
    elif stat.S_IFMT(mode) == S_IFGITLINK:
        return S_IFGITLINK
    ret = stat.S_IFREG | 0o644
    ret |= (mode & 0o111)
    return ret


class Sha1Reader(object):

    def __init__(self, f):
        self.f = f
        self.sha1 = hashlib.sha1()

    def read(self, num):
        data = self.f.read(num)
        self.sha1.update(data)
        return data

    def checksum(self):
        assert self.f.read(20) == self.sha1.digest() 

    def close(self):
        return self.f.close()

    def tell(self):
        return self.f.tell()
    
class Sha1Writer(object):

    def __init__(self, f):
        self.f = f
        self.sha1 = hashlib.sha1()

    def write(self, data):
        self.sha1.update(data)
        self.f.write(data)
        
    def close(self):
        sha = self.sha1.digest()
        self.f.write(sha)
        self.f.close()

    def tell(self):
        return self.f.tell()
