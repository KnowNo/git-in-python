'''
Created on Jun 19, 2014

@author: lzrak47
'''

import os

GIT_DIR = '.git'
    
INDEX_PATH = os.path.join(GIT_DIR, 'index')

HEAD_PATH = os.path.join(GIT_DIR, 'HEAD')

CONFIG_PATH = os.path.join(GIT_DIR, 'config')

GITIGNORE_PATH = '.gitignore'

DESCRIPTION_PATH = os.path.join(GIT_DIR, 'description')

BRANCHES_DIR = os.path.join(GIT_DIR, 'branches')

HOOK_DIR = os.path.join(GIT_DIR, 'hook')
    
OBJECT_DIR = os.path.join(GIT_DIR, 'objects')
OBJECT_INFO_DIR = os.path.join(OBJECT_DIR, 'info')
OBJECT_PACK_DIR = os.path.join(OBJECT_DIR, 'pack')

INFO_DIR = os.path.join(GIT_DIR, 'info')
INFO_EXCLUDE_PATH = os.path.join(INFO_DIR, 'exclude')

REF_DIR = os.path.join(GIT_DIR, 'refs')
REF_HEADS_DIR = os.path.join(REF_DIR, 'heads')
REF_TAG_DIR = os.path.join(REF_DIR, 'tag')

INIT_DIR = [
    BRANCHES_DIR,
    HOOK_DIR,
    INFO_DIR,
    OBJECT_DIR,
    OBJECT_PACK_DIR,
    OBJECT_INFO_DIR,
    REF_DIR,
    REF_HEADS_DIR,
    REF_TAG_DIR,
]

INIT_FILE = [
    [HEAD_PATH, 'ref: refs/heads/master'],
    [DESCRIPTION_PATH, 'Unnamed repository'],
    [INFO_EXCLUDE_PATH, ''],
]
