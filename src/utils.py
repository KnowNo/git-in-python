'''
Created on Jun 9, 2014

@author: lzrak47
'''

from difflib import unified_diff
import hashlib
import os
import stat
import tempfile

import pathspec
from termcolor import colored

from constants import GITIGNORE_PATH


S_IFGITLINK = 0o160000

def write_to_file(path, content, mode=None):       
    dir = os.path.dirname(path)
    
    if dir and not os.path.exists(dir):
        os.makedirs(dir)
        
    with open(path, 'w') as f:
        f.write(content)
        
    if mode:
        os.chmod(path, mode)
    
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
    
def diff_file(old_file, new_file):
    if old_file['path']:
        print_str = 'diff --git a/%s b/%s\n' % (old_file['path'], old_file['path'])
    else:
        print_str = 'diff --git a/%s b/%s\n' % (new_file['path'], new_file['path'])
    
    if old_file['mode'] == new_file['mode']:
        print_str += 'index %.7s..%.7s %04o\n' % (old_file['sha1'], new_file['sha1'], new_file['mode']) 
        
    elif not old_file['mode']:
        print_str += 'new file mode %04o\n' % (new_file['mode'])
        print_str += 'index %.7s..%.7s\n' % (old_file['sha1'], new_file['sha1'])
    
    elif not new_file['mode']:
        print_str += 'deleted file mode %04o\n' % (old_file['mode'])
        print_str += 'index %.7s..%.7s\n' % (old_file['sha1'], new_file['sha1'])
             
    else:
        print_str += 'old mode %04o\n' % (old_file['mode'])
        print_str += 'new mode %04o\n' % (new_file['mode'])
        print_str += 'index %.7s..%.7s\n' % (old_file['sha1'], new_file['sha1'])
       
    from_file = 'a/%s' % old_file['path'] if old_file['path'] else '/dev/null'
    to_file = 'b/%s' % new_file['path'] if new_file['path'] else '/dev/null'
    for i, line in enumerate(unified_diff(old_file['content'].splitlines(), new_file['content'].splitlines(), fromfile=from_file , tofile=to_file)):
        str = '%s\n' % line.strip('\n')
        if line.startswith('@@'):
            print_str += colored(str, 'cyan')
        elif line.startswith('+') and i >= 2:
            print_str += colored(str, 'green')
        elif line.startswith('-') and i >= 2:
            print_str += colored(str, 'red')
        else:
            print_str += str
    return print_str

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
