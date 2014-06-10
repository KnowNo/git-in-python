'''
Created on Jun 9, 2014

@author: lzrak47
'''

def write_to_file(file_name, content):
    f = open(file_name, 'w')
    f.write(content)
    f.close()
