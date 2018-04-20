import io
import os
import re
import sys

import argparse
import platform

year_regex = re.compile(r'/[0-9]{2}/[0-9]{2}/')

def main(path, extensions):
    print(path)
    print(extensions)

    files = get_files(path, extensions)

    for f in files:
        new_name = correct_name(f)
        print('{old}\n  -> {new}'.format(old=f, new=new_name))

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

    return args.directory, extensions_str
    
def get_files(path, extensions):
    walk_data = os.walk(path)
    found = []

    for root, dirs, files in walk_data:
        if len(dirs) is 0:
            found = found + ['{r}/{f}'.format(r=root, f=f) for f in files]

    r = re.compile(r'^.*/[0-9]{2}/[0-9]{2}/.*\.' + extensions + '$')
    return [f for f in found if r.match(f)]
            
def correct_name(path):
    name, extension = get_name(path)
    root = get_root(path)
    year = get_year(path)
    name = name.replace(year, '')
    name = get_normalized_name(name) + extension
    
    return "{r}/[{y}] {n}".format(r=root, y=year, n=name)

def get_root(path):
    root = os.path.dirname(path) + '/'
    year = year_regex.search(root)
    return root[:year.span()[0]]

def get_year(path):
    year = year_regex.search(path) 
    year = path[year.span()[0]:year.span()[1]]

    return ''.join(year.split('/'))

def get_name(path):
    ext = path.rfind('.')
    return path[path.rfind('/') + 1:ext], path[ext:]

def get_normalized_name(name):
    name = name.lower()
    for c in ['-', '_', '[', ']']:
        if c in name:
            name = name.replace(c, ' ')

    name = name.strip()
    name = '_'.join(name.split())
    return name

def rename(old, new):
    os.rename(old, new)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(sys.argv[0])

    argparser.add_argument('-d', '--directory', type=str, default='.')

    argparser.add_argument('-P', '--pdf',  action='store_true', default=False)
    argparser.add_argument('-T', '--txt',  action='store_true', default=False)
    argparser.add_argument('-D', '--doc',  action='store_true', default=False)
    argparser.add_argument('-G', '--gdoc', action='store_true', default=False)
    argparser.add_argument('--all', action='store_true')

    args = argparser.parse_args()
    validate_args(args)
    main(*prepare_args(args))

