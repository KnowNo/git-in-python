'''
Created on Jul 4, 2014

@author: lzrak47
'''
import os
import shutil
import unittest

from command import Command
from objects import Blob
from repository import Repository
from utils import write_to_file, get_file_mode


class TestAdd(unittest.TestCase):


    def setUp(self):
        self.workspace = 'test_add'
        Command.cmd_init(self.workspace)


    def tearDown(self):
        os.chdir('..')
        shutil.rmtree(self.workspace)

    def _check_blob_and_index(self, *paths_contents):
        entries = Repository().index.entries
        for path, content in paths_contents:
            sha1 = Blob(content).sha1
            blob = Blob(sha1=sha1)
            self.assertEqual(blob.raw_content, content)
            self.assertEqual(entries[path]['sha1'], sha1)
            self.assertEqual(entries[path]['mode'], get_file_mode(path))
        
    def test_add_file(self):
        path = '1.txt'
        content = '1\n'
        write_to_file(path, content)
        Command.cmd_add(path)
        self._check_blob_and_index((path, content))
        
    def test_add_dir(self):
        path = os.path.join('dir', '2.txt')
        content = '2\n'
        write_to_file(path, content)
        Command.cmd_add(path)
        self._check_blob_and_index((path, content))
       
    def test_add_all(self):
        paths_contents = [('1.txt', '1\n'), (os.path.join('dir', '2.txt'), '2\n')]
        for path, content in paths_contents:
            write_to_file(path, content)
        Command.cmd_add('.')
        self._check_blob_and_index(*paths_contents)

if __name__ == "__main__":
    unittest.main()