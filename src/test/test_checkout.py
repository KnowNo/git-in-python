'''
Created on Jul 4, 2014

@author: lzrak47
'''
import os
import shutil
import unittest

from branch import Branch
from command import Command
from utils import write_to_file, read_file


class TestCheckout(unittest.TestCase):


    def setUp(self):
        self.workspace = 'test_branch'
        Command.cmd_init(self.workspace)
        Command.cmd_commit('first ci')
        self.file_list = [('1.txt', '1\n'), ('2.txt', '2\n')]
        for path, content in self.file_list:
            write_to_file(path, content)
            Command.cmd_add(path)
        Command.cmd_commit('master ci')
        
        self.new_branch = 'new_branch'
        Command.cmd_branch(self.new_branch)


    def tearDown(self):
        os.chdir('..')
        shutil.rmtree(self.workspace)


    def test_checkout(self):
        Command.cmd_checkout(self.new_branch)
        self.assertEqual(Branch().head_name, self.new_branch)
        
        write_to_file(self.file_list[0][0], '11\n')
        Command.cmd_rm(self.file_list[1][0])
        new_path = '3.txt'
        new_content = '3\n'
        write_to_file(new_path, new_content)
        Command.cmd_add('.')
        Command.cmd_commit('branch ci')
        
        Command.cmd_checkout('master')
        self.assertTrue(os.path.exists(self.file_list[1][0]))
        self.assertFalse(os.path.exists(new_path))
        self.assertEqual(read_file(self.file_list[0][0]), self.file_list[0][1])


if __name__ == "__main__":
    unittest.main()