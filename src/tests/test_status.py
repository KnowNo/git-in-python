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


class TestStatus(unittest.TestCase):


    def setUp(self):
        self.workspace = 'test_status'
        Command.cmd_init(self.workspace)

    def tearDown(self):
        os.chdir('..')
        shutil.rmtree(self.workspace)

    def test_status_init(self):
        repo = Repository()
        untracked_files = repo.get_untracked_files()
        self.assertFalse(untracked_files)
        Command.cmd_status()
        
    def test_status_untracked_files(self):
        path, content = ('1.txt', '1\n')
        write_to_file(path, content)
        repo = Repository()
        untracked_files = repo.get_untracked_files()
        self.assertEqual(untracked_files, ['1.txt'])
        Command.cmd_status()
        
    def test_status_unstaged_files(self):
        file_list = [('1.txt', '1\n'), ('2.txt', '2\n')]
        for path, content in file_list:
            write_to_file(path, content)
            Command.cmd_add(path)
        
        write_to_file(file_list[0][0], '11\n')
        os.remove(file_list[1][0])
        
        repo = Repository()
        unstaged_files = repo.get_unstaged_files()
        
        self.assertEqual(unstaged_files['modified'], [file_list[0][0]])
        self.assertEqual(unstaged_files['deleted'], [file_list[1][0]])
        Command.cmd_status()
        
    def test_status_uncommitted_files(self):
        file_list = [('1.txt', '1\n'), ('2.txt', '2\n')]
        for path, content in file_list:
            write_to_file(path, content)
            Command.cmd_add(path)
        Command.cmd_commit('first ci')
        
        write_to_file(file_list[0][0], '11\n')
        Command.cmd_rm(file_list[1][0])
        new_path = '3.txt'
        new_content = '3\n'
        write_to_file(new_path, new_content)
        Command.cmd_add('.')
        
        repo = Repository()
        uncommitted_files = repo.get_uncommitted_files()
        self.assertEqual(uncommitted_files['modified'], [file_list[0][0]])
        self.assertEqual(uncommitted_files['deleted'], [file_list[1][0]])
        self.assertEqual(uncommitted_files['new file'], [new_path])
        Command.cmd_status()
        

if __name__ == "__main__":
    unittest.main()