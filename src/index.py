'''
Created on Jun 14, 2014

@author: lzrak47
'''
import binascii
from collections import OrderedDict
import os
import stat
import struct

from objects import Tree
from utils import Sha1Reader, Sha1Writer, write_object_to_file


class Index(object):
    '''
    git index file: https://github.com/git/git/blob/master/Documentation/technical/index-format.txt
    '''

    def __init__(self, path):
        self.path = path
        self.entries = OrderedDict()
        if os.path.exists(path):
            self._parse_file()

    
    def _parse_header(self, f):
        header = f.read(4)
        assert header == 'DIRC'
        version, entries_num = struct.unpack('>LL', f.read(4 * 2))
        assert version in (1, 2)
        return entries_num
    
    
    def add_entry(self, name, **kwargs):
        self.entries[name] = kwargs
        
    def _parse_entries(self, f):
        begin = f.tell()
        ctime = struct.unpack(">LL", f.read(8))
        mtime = struct.unpack(">LL", f.read(8))
        (dev, ino, mode, uid, gid, size, sha1, flags, ) = struct.unpack(">LLLLLL20sH", f.read(4 * 6 + 20 + 2))
        name = f.read((flags & 0x0fff))
        #several '\0'
        real_size = ((f.tell() - begin + 8) & ~7)
        f.read((begin + real_size) - f.tell())
        
        self.add_entry(name, ctime=ctime, mtime=mtime, dev=dev, ino=ino, mode=mode, \
                       uid=uid, gid=gid, size=size,sha1=binascii.hexlify(sha1), flags=flags & ~0x0fff)
    
    def _parse_file(self):
        f = Sha1Reader(open(self.path, 'rb'))
        entries_num = self._parse_header(f)
        for i in xrange(entries_num):  # @UnusedVariable i
            self._parse_entries(f)
        
        #trick
        f.read(os.path.getsize(self.path)-f.tell()-20)
        
        f.checksum()
        f.close()
    
    def _write_header(self, f):
        f.write("DIRC")
        f.write(struct.pack(">LL", 2, len(self.entries)))
    
    def _write_time(self, f, t):
        if isinstance(t, int):
            t = (t, 0)
        elif isinstance(t, float):
            (secs, nsecs) = divmod(t, 1.0)
            t = (int(secs), int(nsecs * 1000000000))
        f.write(struct.pack(">LL", *t))
        
    def _write_entries(self, f):
        for name, properties in self.entries.iteritems():
            begin = f.tell()
            self._write_time(f, properties['ctime'])
            self._write_time(f, properties['mtime'])
            flags = len(name) | (properties['flags'] &~ 0x0fff)
            f.write(struct.pack(">LLLLLL20sH", properties['dev'] & 0xFFFFFFFF, properties['ino'] & 0xFFFFFFFF, \
                                 properties['mode'], properties['uid'], properties['gid'], properties['size'], \
                                 binascii.unhexlify(properties['sha1']), flags))
            f.write(name)
            real_size = ((f.tell() - begin + 8) & ~7)
            f.write('\0' * ((begin + real_size) - f.tell()))
    
    def write_to_file(self):
        # copy-on-write
        lock_file = self.path + '.lock'
        f = Sha1Writer(open(lock_file, 'wb'))
        self._write_header(f)
        self._write_entries(f)
        f.close()
        os.rename(lock_file, self.path)
    

    def do_commit(self):
        tree = {}
        for path, property in self.entries.iteritems():
            t = tree
            path_arr = path.split('/')
            for path_ele in path_arr[:-1]:
                t = t.setdefault(path_ele, {})
            t = t.setdefault(path_arr[-1], (property['mode'], property['sha1']))
        def _build_tree(path):
            dir_arr = []
            file_arr = []
            for name, entry in path.iteritems():
                if isinstance(entry, dict):
                    mode = stat.S_IFDIR
                    sha1 = _build_tree(entry).sha1
                    dir_arr.append({'name':name, 'mode':mode, 'sha1':sha1})
                else:
                    (mode, sha1) = entry
                    file_arr.append({'name':name, 'mode':mode, 'sha1':sha1})
            newtree = Tree(sorted(dir_arr,key = lambda x:x['name']) + sorted(file_arr,key = lambda x:x['name']))
            write_object_to_file(newtree.path, newtree.content)
            return newtree
            
        return _build_tree(tree)            
                