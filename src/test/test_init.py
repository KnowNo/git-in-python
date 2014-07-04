'''
Created on Jul 2, 2014

@author: lzrak47
'''
import os
import shutil
import unittest

from command import Command
from constants import GIT_DIR, INIT_DIR, INIT_FILE
from utils import read_file


class TestInit(unittest.TestCase):

    def _check_dirs_and_files(self, workspace):
        Command.cmd_init(workspace)
        self.assertTrue(os.path.exists(GIT_DIR))
        for dir in INIT_DIR:
            self.assertTrue(os.path.exists(dir))
        for file in INIT_FILE:
            path = file[0]
            content = file[1]
            self.assertEqual(read_file(path), content)
            
    def test_init_with_workspace(self):
        workspace = 'test_init'
        self._check_dirs_and_files(workspace)
        os.chdir('..')
        shutil.rmtree(workspace)
            
    def test_init_without_workspace(self):
        workspace = './'
        self._check_dirs_and_files(workspace)
        shutil.rmtree(GIT_DIR)


if __name__ == "__main__":
    unittest.main()
