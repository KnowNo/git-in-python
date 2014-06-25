'''
Created on Jun 9, 2014

@author: lzrak47
'''
import os
import time

from termcolor import colored

from branch import Branch
from config import Config
from constants import INDEX_PATH, GIT_DIR, INIT_DIR, \
    INIT_FILE, CONFIG_PATH
from index import Index
from objects import Blob, Commit, Tree
from utils import get_all_files_in_dir, read_file, write_to_file, cal_mode, \
    less_str, filter_by_gitignore, get_file_mode


class Repository(object):
    '''
    The git repository
    '''
    def __init__(self):
        self.index = Index(INDEX_PATH)
        self.working_tree_files = get_all_files_in_dir('.', GIT_DIR)
        self.config = Config()
        self.branch = Branch()

    def stage(self, files):
        try:
            for file in files:
                content = read_file(file)
                blob = Blob(content)
                if not os.path.exists(blob.path):
                    write_to_file(blob.path, blob.content)
                stat = os.stat(os.path.join(file))
                self.index.set_entry(file, ctime=stat.st_ctime, mtime=stat.st_mtime, dev=stat.st_dev, ino=stat.st_ino, mode=cal_mode(stat.st_mode), \
                       uid=stat.st_uid, gid=stat.st_gid, size=stat.st_size, sha1=blob.sha1, flags=0)
            self.index.write_to_file()
            self.index = Index(INDEX_PATH)

        except Exception, e:
            print 'stage file %s error: %s' % (file, e)

    @staticmethod
    def create_repository(workspace, bare=False):
        if not os.path.exists(workspace):
            os.mkdir(workspace)
        os.chdir(workspace)

        if not bare:
            os.mkdir(GIT_DIR)

        for new_dir in INIT_DIR:
            os.mkdir(new_dir)

        for file_and_content in INIT_FILE:
            file_name = file_and_content[0]
            content = file_and_content[1]
            write_to_file(file_name, content)


        init_config_dict = {
            'core': {
                'repositoryformatversion' : '0',
                'filemode' : 'true',
                'bare' : str(bare).lower(),
                'logallrefupdates' : 'true',
            }
        }

        content = Config.create_config(init_config_dict)
        write_to_file(CONFIG_PATH, content)

    def commit(self, msg):
        new_tree = self.index.do_commit()

        committer_name = self.config.config_dict['user']['name']
        committer_email = '<%s>' % (self.config.config_dict['user']['email'])
        commit_time = int(time.time())
        commit_timezone = time.strftime("%z", time.gmtime())

        commit = Commit(sha1=None, tree_sha1=new_tree.sha1, parent_sha1=self.branch.head_commit, name=committer_name, email=committer_email, \
                        timestamp=commit_time, timezone=commit_timezone, msg=msg)
        write_to_file(commit.path, commit.content)
        write_to_file(self.branch.head_path, commit.sha1)

    def delete(self, file):
        del self.index.entries[file]
        self.index.write_to_file()

    def show_log(self, num):
        cur_commit = Commit(sha1=self.branch.head_commit)
        print_str = cur_commit.raw_content
        while num > 1 and cur_commit.parent_sha1:
            num -= 1
            parent_commit = Commit(sha1=cur_commit.parent_sha1)
            print_str += '\n%s' % (parent_commit.raw_content)
            cur_commit = parent_commit
        less_str(print_str)

    def _get_untracked_files(self):
        raw_list = list(set(self.working_tree_files).difference(set(list(self.index.entries))))
        return filter_by_gitignore(raw_list)

    def _get_unstaged_files(self):
        res = {
            'modified': [],
            'deleted' : [],
        }
        for name, properties in self.index.entries.iteritems():
            if name not in self.working_tree_files:
                res['deleted'].append(name)
            elif get_file_mode(name) != properties['mode'] or Blob(read_file(name)).sha1 != properties['sha1']:
                res['modified'].append(name)

        return res


    def _get_uncommitted_files(self):
        if not self.branch.head_commit:
            return {'new file' : self.index.entries}

        tree = Tree(sha1=Commit(sha1=self.branch.head_commit).tree)
        tree_objects = tree.parse_objects()
        return {
            'modified': [name for name in set(self.index.entries).intersection(set(tree_objects)) \
                         if self.index.entries[name]['sha1'] != tree_objects[name]['sha1'] or \
                         self.index.entries[name]['mode'] != tree_objects[name]['mode']],
            'deleted' : set(tree_objects).difference(self.index.entries),
            'new file' : set(self.index.entries).difference(set(tree_objects)),
        }

    def show_status(self):
        untracked_files = self._get_untracked_files()
        unstaged_files = self._get_unstaged_files()
        uncommitted_files = self._get_uncommitted_files()
        print_str = 'On branch %s\n' % (self.branch.head_name)
        
        if uncommitted_files['modified'] or uncommitted_files['deleted'] or uncommitted_files['new file']:
            print_str += 'Changes to be committed:\n  (use "git reset HEAD <file>..." to unstage)\n\n'
            for change, files in uncommitted_files.iteritems():
                for file in files:
                    print_str += colored('\t%s:\t%s\n' % (change, file), 'green')
            print_str += '\n'
        else:
            print_str += '\nno changes added to commit\n\n'
            
        
        if unstaged_files['modified'] or unstaged_files['deleted']:
            print_str += 'Changes not staged for commit:\n  (use "git add <file>..." to update what will be committed)\n'
            print_str += '  (use "git checkout -- <file>..." to discard changes in working directory)\n\n'
            for change, files in unstaged_files.iteritems():
                for file in files:
                    print_str += colored('\t%s:\t%s\n' % (change, file), 'red')
            print_str += '\n'
            
        
        if untracked_files:
            print_str += 'Untracked files:\n  (use "git add <file>..." to include in what will be committed)\n\n'
            for file in untracked_files:
                print_str += colored('\t%s\n' % file, 'red')
            print_str += '\n'

        print print_str
    
    def update_head_commit(self, commit_sha1):
        write_to_file(self.branch.head_path, commit_sha1)
    
    def rebuild_index_from_commit(self, commit_sha1):
        tree = Tree(sha1=Commit(sha1=commit_sha1).tree)
        tree_objects = tree.parse_objects()
        
        for name in set(self.index.entries).difference(set(tree_objects)): 
            self.index.entries.pop(name)
        
        for name, properties in tree_objects.iteritems():
            if not self.index.entries.has_key(name) or properties['sha1'] != self.index.entries[name]['sha1'] or \
                properties['mode'] != self.index.entries[name]['mode']:
                self.index.set_entry(name, ctime=0.0, mtime=0.0, dev=0, ino=0, mode=properties['mode'], \
                   uid=0, gid=0, size=0, sha1=properties['sha1'], flags=0)
            
        self.index.write_to_file()
        self.index = Index(INDEX_PATH)
    
    def rebuild_working_tree(self):
        for path, properties in self.index.entries.iteritems():
            content = Blob(sha1=properties['sha1']).raw_content
            write_to_file(path, content, mode=properties['mode'])
            
        
        
        
        
        
        
        
