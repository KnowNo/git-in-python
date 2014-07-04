#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Jun 8, 2014

@author: lzrak47
'''

import argparse
import sys

from command import Command


class Parser(object):
    '''
    parse args from command line.
    '''

    def __init__(self, argv):
        self.argv = argv
        self.commands = {
            'init' : {
                'func' : self._init,
                'help' : 'Create an empty Git repository or reinitialize an existing one',
                'args' : [
                    {
                        'name' : ['directory'],
                        'properties' :
                        {
                            'help' : 'Directory of the git repository',
                            'nargs' : '?', 
                            'default' : './',
                        },
                    },
                ]
            },
                    
            'add' : {
                'func' : self._add,
                'help' : 'Add file contents to the index',
                'args' : [
                    {
                        'name' : ['file'],
                        'properties' :
                        {
                            'help' : 'Files to add content from',
                        },
                    },
                ]
            },
                         
            'rm' : {
                'func' : self._rm,
                'help' : 'Remove files from the working tree and from the index',
                'args' : [
                    {
                        'name' : ['file'],
                        'properties' :
                        {
                            'help' : 'Files to remove',
                        },
                    },
                    {
                        'name' : ['--cached'],
                        'properties' :
                        {
                            'help' : 'Remove files only from the index',
                            'action' : 'store_true',
                        },
                    },
                ]
            },
                    
            'commit' : {
                'func' : self._commit,
                'help' : 'Record changes to the repository',
                'args' : [
                    {
                        'name' : ['-m', '--message'],
                        'properties' :
                        {
                            'help' : 'Use the given msg as the commit message',
                            'dest' : 'msg',
                        }
                    }
                ],
            },
                    
            'log' : {
                'func' : self._log,
                'help' : 'Show commit logs',
                'args' : [
                    {
                        'name' : ['-n'],
                        'properties' :
                        {
                            'help' : 'Limit the number of commits to output',
                            'nargs' : '?', 
                            'type' : int, 
                            'dest' : 'num',
                            'default' : float('infinity'),
                        }
                    },
                ],
            },
                         
            'status' : {
                'func' : self._status,
                'help' : 'Show the working tree status',
                'args' : [],
            },
                         
            'branch' : {
                'func' : self._branch,
                'help' : 'List, create, or delete branches',
                'args' : [
                    {
                        'name' : ['name'],
                        'properties' :
                        {
                            'help' : 'The name of the branch to create or delete',
                            'nargs' : '?', 
                            'default' : '',
                        }
                    },
                    {
                        'name' : ['-d'],
                        'properties' :
                        {
                            'help' : 'Delete a branch.',
                            'action' : 'store_true',
                            'dest' : 'is_deleted',
                        }
                    }
                ],
            },
            'reset' : {
                'func' : self._reset,
                'help' : 'Reset current HEAD to the specified state',
                'args' : [
                    {
                        'name' : ['commit_sha1'],
                        'properties' :
                        {
                            'help' : 'Commit to reset',
                        }
                    },
                    {
                        'name' : ['--soft'],
                        'properties' :
                        {
                            'help' : 'Does not touch the index file or the working tree at all',
                            'action' : 'store_true',
                        }
                    },
                    {
                        'name' : ['--hard'],
                        'properties' :
                        {
                            'help' : 'Resets the index and working tree',
                            'action' : 'store_true',
                        }
                    },
                ],
            },
            'checkout' : {
                'func' : self._checkout,
                'help' : 'Checkout a branch to the working tree',
                'args' : [
                    {
                        'name' : ['branch'],
                        'properties' :
                        {
                            'help' : 'Branch to checkout',
                        }
                    },
                ],
            },
            'diff' : {
                'func' : self._diff,
                'help' : 'Show changes between commits, commit and working tree, etc',
                'args' : [
                    {
                        'name' : ['--cached'],
                        'properties' :
                        {
                            'help' : 'Show changes between and the index and the head tree',
                            'action' : 'store_true',
                        }
                    },
                ],
            },
            'push' : {
                'func' : self._push,
                'help' : 'Update remote refs along with associated objects',
                'args' : [],
            },
                    
            'clone' : {
                'func' : self._clone,
                'help' : 'Clone a repository into a new directory',
                'args' : [],
            },
    }

    def _init(self, args):
        Command.cmd_init(workspace=args.directory)

    def _add(self, args):
        Command.cmd_add(args.file)
        
    def _rm(self, args):
        Command.cmd_rm(args.file, args.cached)

    def _commit(self, args):
        Command.cmd_commit(args.msg)

    def _log(self, args):
        Command.cmd_log(args.num)
        
    def _status(self, args):
        Command.cmd_status()
    
    def _branch(self, args):
        Command.cmd_branch(args.name, args.is_deleted)
    
    def _reset(self, args):
        Command.cmd_reset(args.commit_sha1, is_soft=args.soft, is_hard=args.hard)
        
    def _checkout(self, args):
        Command.cmd_checkout(args.branch)
    
    def _diff(self, args):
        Command.cmd_diff(args.cached)
    
    def _push(self, args):
        pass

    def _clone(self, args):
        pass

    def parse(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()
        
        for name, detail in self.commands.iteritems():
            subparser = subparsers.add_parser(name, help=detail['help'])
            for arg in detail['args']:
                subparser.add_argument(*arg['name'], **arg['properties'])
                
        args_res = parser.parse_args()
        self.commands[sys.argv[1]]['func'](args_res)


if __name__ == '__main__':
    p = Parser(sys.argv)
    p.parse()
