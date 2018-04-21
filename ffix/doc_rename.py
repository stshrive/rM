import os
import sys

import hashlib
import curses

from hashfile import HashedFile

_default_hasher = hashlib.md5
_default_block  = 65536

docs = {}

def _get_hasher(hasher=None):
    return _default_hasher if hasher is None else hasher


def _get_block(block=None):
    return _default_block if block is None else block


def _load_docs(save_root):
    '''
    Loads all docs within the target directory and creates
    a content hash for duplicate checking.
    '''
    if len(docs) == 0:
        print(save_root)
        for f in [f for f in os.listdir(save_root) if os.path.isfile(save_root + f)]:
            sf = '{root}/{filename}'.format(root=save_root, filename=f)
            hf = HashedFile(sf, _get_hasher(), _get_block())
            docs[hf.id] = hf.name


def _rename(old, new):
    '''
    Renames old to new and prompts user when a duplicate file is detected.
    Files do not need to have the same name to be considered duplicates.
    '''
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


def get_name(path):
    '''
    Returns the filename (without extension) and the associated extension
    '''
    ext = path.rfind('.')
    return path[path.rfind('/') + 1:ext], path[ext:]


def normalize_name(name):
    '''
    Given a filename, removes brackets, dashes and spaces and
    replaces them with underscores.
    '''
    name = name.lower()
    for c in ['-', '_', '[', ']']:
        if c in name:
            name = name.replace(c, ' ')

    name = name.strip()
    name = '_'.join(name.split())
    return name
