'''
Created on Jul 4, 2014

@author: lzrak47
'''
import os
import shutil
import unittest

from branch import Branch
from command import Command
from repository import Repository
from utils import write_to_file, read_file


class Test(unittest.TestCase):


    def setUp(self):
        self.workspace = 'test_reset'
        Command.cmd_init(self.workspace)
        
        self.path, self.content = ('1.txt', '1\n')
        write_to_file(self.path, self.content)
        Command.cmd_add(self.path)
        Command.cmd_commit('first ci')
        self.first_commit = Branch().head_commit
        
        write_to_file(self.path, '2.txt')
        Command.cmd_add(self.path)
        Command.cmd_commit('second ci')


    def tearDown(self):
        os.chdir('..')
        shutil.rmtree(self.workspace)


    def test_reset_soft(self):
        Command.cmd_reset(self.first_commit, is_soft=True, is_hard=False)
        self.assertEqual(Branch().head_commit, self.first_commit)
        repo = Repository()
        uncommitted_files = repo.get_uncommitted_files()
        unstaged_files = repo.get_unstaged_files()
        self.assertIn(self.path, uncommitted_files['modified'])
        self.assertFalse(unstaged_files['modified'])
        
    def test_reset_default(self):
        Command.cmd_reset(self.first_commit, is_soft=False, is_hard=False)
        self.assertEqual(Branch().head_commit, self.first_commit)
        repo = Repository()
        uncommitted_files = repo.get_uncommitted_files()
        unstaged_files = repo.get_unstaged_files()
        self.assertFalse(uncommitted_files['modified'])
        self.assertIn(self.path, unstaged_files['modified'])
        
    def test_reset_hard(self):
        Command.cmd_reset(self.first_commit, is_soft=False, is_hard=True)
        self.assertEqual(Branch().head_commit, self.first_commit)
        repo = Repository()
        uncommitted_files = repo.get_uncommitted_files()
        unstaged_files = repo.get_unstaged_files()
        self.assertFalse(uncommitted_files['modified'])
        self.assertFalse(unstaged_files['modified'])
        self.assertEqual(read_file(self.path), self.content)


if __name__ == "__main__":
    unittest.main()