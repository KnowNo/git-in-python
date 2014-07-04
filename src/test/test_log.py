'''
Created on Jul 4, 2014

@author: lzrak47
'''
import os
import shutil
import unittest

from command import Command
from utils import write_to_file


class TestLog(unittest.TestCase):


    def setUp(self):
        self.workspace = 'test_log'
        Command.cmd_init(self.workspace)
        
        self.path = '1.txt'
        self.content = '1\n'
        write_to_file(self.path, self.content)
        
        Command.cmd_add(self.path)
        Command.cmd_commit('first ci')
        
        second_content = '11\n'
        write_to_file(self.path, second_content)
        
        Command.cmd_add(self.path)
        Command.cmd_commit('second ci')


    def tearDown(self):
        os.chdir('..')
        shutil.rmtree(self.workspace)


    def test_log_without_num(self):
        Command.cmd_log(float('infinity'), False)
        
    def test_log_with_num(self):
        Command.cmd_log(1, False)


if __name__ == "__main__":
    unittest.main()