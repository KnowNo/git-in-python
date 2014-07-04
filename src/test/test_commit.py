'''
Created on Jul 4, 2014

@author: lzrak47
'''
import os
import shutil
import unittest

from branch import Branch
from command import Command
from objects import Commit, Tree, Blob
from utils import write_to_file


class TestCommit(unittest.TestCase):


    def setUp(self):
        self.workspace = 'test_commit'
        Command.cmd_init(self.workspace)
        self.path = '1.txt'
        self.content = '1\n'
        write_to_file(self.path, self.content)
        Command.cmd_add(self.path)


    def tearDown(self):
        os.chdir('..')
        shutil.rmtree(self.workspace)


    def test_commit_once(self):
        Command.cmd_commit('first ci')
        commit = Commit(sha1=Branch().head_commit)
        self.assertIsNone(commit.parent_sha1)
        tree = Tree(sha1=commit.tree)
        objects = tree.parse_objects()
        self.assertEqual(objects[self.path]['sha1'], Blob(self.content).sha1)
        
    def test_commit_twice(self):
        Command.cmd_commit('first ci')
        parent_sha1 = Branch().head_commit
        
        second_content = '11\n'
        write_to_file(self.path, second_content)
        
        new_path = '2.txt'
        new_content = '2\n'
        write_to_file(new_path, new_content)
        
        Command.cmd_add('.')
        Command.cmd_commit('second ci')
        
        commit = Commit(sha1=Branch().head_commit)
        self.assertEqual(parent_sha1, commit.parent_sha1)
        tree = Tree(sha1=commit.tree)
        objects = tree.parse_objects()
        self.assertEqual(objects[self.path]['sha1'], Blob(second_content).sha1)
        self.assertEqual(objects[new_path]['sha1'], Blob(new_content).sha1)


if __name__ == "__main__":
    unittest.main()