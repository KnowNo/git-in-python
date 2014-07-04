'''
Created on Jul 4, 2014

@author: lzrak47
'''
import os
import shutil
import unittest

from branch import Branch
from command import Command


class TestBranch(unittest.TestCase):


    def setUp(self):
        self.workspace = 'test_branch'
        Command.cmd_init(self.workspace)
        Command.cmd_commit('first ci')
        self.new_branch = 'new_branch'


    def tearDown(self):
        os.chdir('..')
        shutil.rmtree(self.workspace)


    def test_branch_add(self):
        Command.cmd_branch(self.new_branch)
        self.assertIn(self.new_branch, Branch().get_all_branches())
        
    def test_branch_delete(self):
        Command.cmd_branch(self.new_branch)
        self.assertIn(self.new_branch, Branch().get_all_branches())
        Command.cmd_branch(self.new_branch, True)
        self.assertNotIn(self.new_branch, Branch().get_all_branches())
        
    def test_branch_list(self):
        Command.cmd_branch('')
        Command.cmd_branch(self.new_branch)
        Command.cmd_branch('')


if __name__ == "__main__":
    unittest.main()