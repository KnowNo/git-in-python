'''
Created on Jun 9, 2014

@author: lzrak47
'''

import hashlib
import sys

def write_to_file(path, content):
    f = open(path, 'w')
    f.write(content)
    f.close()
    
def read_file(file_name):
    try:
        f = open(file_name, 'r')
        content = f.read()
        f.close()
        return content
    except Exception, e:
        print "open file %s error: %s" % (file_name, e)
        sys.exit(1)

def calSha1(content):
    sha1 = hashlib.sha1()
    sha1.update(content)
    return sha1.hexdigest()


