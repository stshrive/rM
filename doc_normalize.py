import os
import re

year_regex = re.compile(r'/[0-9]{2}/[0-9]{2}/')
dir_names  = set()
    
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
    root = os.path.dirname(path)
    dir_names.add(root)
    root = root + '/'
    year = year_regex.search(root)
    return root[:year.span()[0]]

def get_year(path):
    year = year_regex.search(path) 
    year = path[year.span()[0]:year.span()[1]]

    return ''.join(year.split('/'))

def get_name(path):
    ext = path.rfind('.')
    return path[path.rfind('/') + 1:ext], path[ext:]


