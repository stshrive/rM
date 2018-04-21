import os
import sys

import hashlib
import curses

from hashfile import HashedFile

_default_hasher = hashlib.md5
_default_block  = 65536

docs = {}

def _get_hasher(hasher=None):
    return _default_hasher() if hasher is None else hasher()

def _get_block(block=None):
    return _default_block if block is None else block

def _load_docs(save_root):
    if len(docs) == 0:
        print(save_root)
        for f in [f for f in os.listdir(save_root) if os.path.isfile(save_root + f)]:
            sf = '{root}/{filename}'.format(root=save_root, filename=f)
            hf = HashedFile(sf, _get_hasher(), _get_block())
            docs[hf.id] = hf.name

def _rename(old, new):
    old_hf = HashedFile(old, _get_hasher(), _get_block())
    if old_hf.id not in docs:
        docs[old_hf.id] = new
        os.rename(old, new)
    else:
        old_name = docs[old_hf.id]
        print('WARNING: Duplicate files detected.')
        print('(1) REPLACE -> {new}\n(2) SKIP    -> {old}'.format(new=new, old=old_name))
        selection = input('> ')

        if selection == 1:
            print("Overwriting file")
            os.rename(old_name, new)
            docs[old_hf.id] = new
        else:
            print("Skipping file")
            os.remove(old)

def safe_rename(old, new):
    save_root = os.path.dirname(new)
    _load_docs(save_root)
    _rename(old, new)
