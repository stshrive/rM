import os
import re

import doc_rename as dr

year_regex = re.compile(r'/[0-9]{2}/[0-9]{2}/')
dirs  = set()
    
def get_files(path, extensions):
    '''
    Recursively finds all files within a directory following the 
    <root>/<year_prefix>/<year_postfix> pattern.
    '''
    walk_data = os.walk(path)
    found = []

    for root, dirs, files in walk_data:
        if len(dirs) is 0:
            found = found + ['{r}/{f}'.format(r=root, f=f) for f in files]

    r = re.compile(r'^.*/[0-9]{2}/[0-9]{2}/.*\.' + extensions + '$')
    return [f for f in found if r.match(f)]
            
def format_name(path):
    '''
    Returns a formatted name for files contained in a directory structure
    following the <root>/<year_prefix>/<year_postfix> pattern
    '''
    name, extension = dr.get_name(path)
    root = get_root(path)
    year = get_year(path)
    name = name.replace(year, '')
    name = dr.normalize_name(name) + extension
    
    return "{r}/[{y}] {n}".format(r=root, y=year, n=name)

def get_root(path):
    '''
    Returns the root directory based on the pattern:
    <root>/<year_prefix>/<year_postfix> 
    '''
    root = os.path.dirname(path)
    dirs.add(root)
    root = root + '/'
    year = year_regex.search(root)
    return root[:year.span()[0]]

def get_year(path):
    year = year_regex.search(path) 
    year = path[year.span()[0]:year.span()[1]]

    return ''.join(year.split('/'))

