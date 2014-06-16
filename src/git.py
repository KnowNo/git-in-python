#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jun 8, 2014

@author: lzrak47
'''

import argparse
import os
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
                            'default' : '',
                        },
                    },
                          
                    {
                        'name' : ['--bare'],
                        'properties' :
                        {
                            'help' : 'Create a bare repository',
                            'action' : 'store_true',
                        }
                    }
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
        workspace = os.path.join(os.getcwd(), args.directory)
        Command.cmd_init(workspace=workspace, bare=args.bare)

    def _add(self, args):
        Command.cmd_add(os.getcwd(), args.file)
        
    def _rm(self, args):
        Command.cmd_rm(os.getcwd(), args.file, args.cached)

    def _commit(self, args):
        Command.cmd_commit(os.getcwd(), args.msg)

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
