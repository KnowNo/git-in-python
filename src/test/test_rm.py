'''
Created on Jul 4, 2014

@author: lzrak47
'''
import os
import shutil
import unittest

from command import Command
from repository import Repository
from utils import write_to_file


class TestRm(unittest.TestCase):


    def setUp(self):
        self.workspace = 'test_rm'
        Command.cmd_init(self.workspace)
        self.path = '1.txt'
        content = '1\n'
        write_to_file(self.path, content)
        Command.cmd_add(self.path)


    def tearDown(self):
        os.chdir('..')
        shutil.rmtree(self.workspace)


    def test_rm_cached(self):
        entries = Repository().index.entries
        self.assertIn(self.path, entries)
        Command.cmd_rm(self.path, True)
        entries = Repository().index.entries
        self.assertNotIn(self.path, entries)
        
    def test_rm_no_cached(self):
        entries = Repository().index.entries
        self.assertIn(self.path, entries)
        Command.cmd_rm(self.path, False)
        entries = Repository().index.entries
        self.assertNotIn(self.path, entries)
        self.assertFalse(os.path.exists(self.path))


if __name__ == "__main__":
    unittest.main()