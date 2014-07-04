'''
Created on Jul 4, 2014

@author: lzrak47
'''
import os
import shutil
import unittest

from command import Command
from utils import write_to_file


class TestDiff(unittest.TestCase):


    def setUp(self):
        self.workspace = 'test_diff'
        Command.cmd_init(self.workspace)
        self.old_content = '''
            The Way that can be told of is not the eternal Way;
            The name that can be named is not the eternal name.
            The Nameless is the origin of Heaven and Earth;
            The Named is the mother of all things.
            Therefore let there always be non-being,
              so we may see their subtlety,
            And let there always be being,
              so we may see their outcome.
            The two are the same,
            But after they are produced,
              they have different names.
        '''
        self.new_content = '''
            The Nameless is the origin of Heaven and Earth;
            The named is the mother of all things.
            
            Therefore let there always be non-being,
              so we may see their subtlety,
            And let there always be being,
              so we may see their outcome.
            The two are the same,
            But after they are produced,
              they have different names.
            They both may be called deep and profound.
            Deeper and more profound,
            The door of all subtleties!
        '''
        self.file_list = [('1.txt', self.old_content), ('2.txt', self.old_content)]
        for path, content in self.file_list:
            write_to_file(path, content)
            Command.cmd_add(path)


    def tearDown(self):
        os.chdir('..')
        shutil.rmtree(self.workspace)


    def test_diff_default(self):
        write_to_file(self.file_list[0][0], self.new_content)
        os.remove(self.file_list[1][0])
        Command.cmd_diff(False, False)
        
    def test_diff_cached(self):
        Command.cmd_commit('first ci')
        write_to_file(self.file_list[0][0], self.new_content)
        Command.cmd_rm(self.file_list[1][0])
        new_path = '3.txt'
        write_to_file(new_path, self.new_content)
        Command.cmd_add('.')
        Command.cmd_diff(True, False)
        

if __name__ == "__main__":
    unittest.main()