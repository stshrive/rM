#!/usr/bin/env python3

import os
import sys
import argparse

import dir_search
import doc_rename

def main(path, extensions, overwrite):
    files = dir_search.get_files(path, extensions)

    for f in files:
        new_name = dir_search.format_name(f)
        print('{old}\n->  {new}'.format(old=f, new=new_name))
        doc_rename.safe_rename(f, new_name,  overwrite)


def cleanup():
    '''
    Removes empty directories from the renamed directory tree.
    '''
    for d in dir_search.dirs:
        parent = os.path.dirname(d)
        if len(os.listdir(d)) == 0:
            os.rmdir(d)

        while len(os.listdir(parent)) == 0:
            os.rmdir(parent)
            parent = os.path.dirname(parent)

def validate_args(args):
    ext = [args.pdf, args.txt, args.doc, args.gdoc]
    if not any(ext) and not args.all:
        raise

    if args.all and any(ext):
        raise

def prepare_args(args):
    ext = [args.pdf, args.txt, args.doc, args.gdoc]

    if args.all:
        extensions_str = '(txt|doc|docx|gdoc|pdf)'
    else:
        extensions_str = '({})'.format('|'.join(list(filter(None,[
            'pdf'if ext[0] else None, 'txt' if ext[1] else None,
            'doc' if ext[2] else None,'docx'if ext[2] else None,'gdoc'if ext[3] else None]))))

    return args.directory, extensions_str, args.force_overwrite

if __name__ == "__main__":
    argparser = argparse.ArgumentParser(sys.argv[0])

    argparser.add_argument('-d', '--directory', type=str, default='.')
    argparser.add_argument('-P', '--pdf',  action='store_true', default=False)
    argparser.add_argument('-T', '--txt',  action='store_true', default=False)
    argparser.add_argument('-D', '--doc',  action='store_true', default=False)
    argparser.add_argument('-G', '--gdoc', action='store_true', default=False)

    argparser.add_argument('--all', action='store_true')
    argparser.add_argument('-R', '--remove-empty', action='store_true', default=False)
    argparser.add_argument('-F', '--force-overwrite', action='store_true', default=False)
    args = argparser.parse_args()
    validate_args(args)
    main(*prepare_args(args))

    if args.remove_empty:
        cleanup()

