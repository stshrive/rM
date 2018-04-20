import os
import sys

import hashlib

from hashfile import HashedFile

_default_hasher = hashlib.md5()
_default_block  = 65536

docs = []

def get_hasher(hasher=None):
    return _default_hasher if hasher is None else hasher

def get_block(block=None):
    return _default_block if block is None else block

def safe_rename(old, new):
    save_root = os.path.dirname(new)
    
    old_hf = HashedFile(old)
    if old_hf in docs

def load_docs(path):
    for f in os.listdir(os.path.dirname(path)):
        sf = '{root}/{filename}'.format(root=save_root, filename=f)
        docs.append(HashedFile(sf))
