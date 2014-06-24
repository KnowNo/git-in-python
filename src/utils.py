'''
Created on Jun 9, 2014

@author: lzrak47
'''

import hashlib
import os
import stat
import tempfile

import pathspec

from constants import GITIGNORE_PATH


S_IFGITLINK = 0o160000

def write_to_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
    
def write_object_to_file(path, content):       
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.mkdir(dir)
    write_to_file(path, content)
    
def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

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

def get_file_mode(path):
    res = os.stat(path)
    return cal_mode(res.st_mode)

def less_str(str):
    with tempfile.NamedTemporaryFile() as f:
        f.write(str)
        f.seek(0)
        os.system("cat %s | less" % f.name)

def get_all_files_in_dir(dir, *exclude_dirs):
    file_list = []
    for root, dirs, files in os.walk(dir):
        for exclude_dir in set(exclude_dirs).intersection(set(dirs)):
            dirs.remove(exclude_dir)
        for file in files:
            file_list.append(os.path.join(root[2:], file))
    return file_list

def filter_by_gitignore(raw_list):
    if not os.path.exists(GITIGNORE_PATH):
        return raw_list
    else:
        with open(GITIGNORE_PATH, 'r') as fh:
            spec = pathspec.PathSpec.from_lines(pathspec.GitIgnorePattern, fh)
        return set(raw_list).difference(spec.match_files(raw_list))

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
