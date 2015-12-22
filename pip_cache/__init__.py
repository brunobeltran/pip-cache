"""
File: pip-cache.py
Author: Bruno Beltran
Email: brunobeltran0@email.com
Github: https://github.com/brunobeltran0
Description: Keeps a local cache of all available PyPi packages. Fast, local,
manually updated version of `pip search`.
"""
from __future__ import print_function
import os
import sys
from .xdg import get_xdg_data_dir
import argparse

#TODO speed up by using msgpack to store a marisa-trie for quick prefix lookup
#import marisa-trie
#import msgpack
pip_cache_data_dir = os.path.join(get_xdg_data_dir(), 'pip-cache')
index_filename = os.path.join(pip_cache_data_dir, 'all-packages.txt')

def filter_prefix(strings, prefix=''):
    return list(filter(lambda x: x.startswith(prefix), strings))

def get_package_names(prefix='', prefix_func=filter_prefix):
    """
    Return a list of packages name strings from cache matching a prefix.
    """
    if not os.path.isfile(index_filename):
        open(index_filename, 'a').close()
    with open(index_filename, 'r') as f:
        packages = f.read().splitlines()
    return prefix_func(packages, prefix=prefix)

def pkgnames(prefix=''):
    matching_packages = get_package_names(prefix=prefix)
    for package in matching_packages:
        print(package)

#TODO: support auto-async updates
# update_interval = timedelta(days=1)
# update_index_now = False
# import time
# from datetime import timedelta
# if not os.path.isfile(index_filename):
#     open(index_filename, 'a').close()
#     update_index_now = True

# now = time.time()
# update_time = os.path.getmtime(index_filename)
# if now - update_time > update_interval.total_seconds():
#     update_index_now = True

# there does not seem to be a good behavior for case when completion is
# attempted during update of index, since blocking to wait for completion seems
# even worse than just using the partial or empty index (and thus failing to
# complete correctly) until the update is done. Thus, we go with the latter
# option, and use no locking of our index file.
def update_package_list():
    try:
        import xmlrpclib
    except ImportError:
        import xmlrpc.client as xmlrpclib
    print('Connecting to PyPi...', end='')
    sys.stdout.flush()
    client = xmlrpclib.ServerProxy('https://pypi.python.org/pypi')
    print('downloading package names...', end='')
    sys.stdout.flush()
    packages = client.list_packages()
    print('done!')
    sys.stdout.flush()
    print('Writing packages to cache...', end='')
    sys.stdout.flush()
    with open(index_filename, 'w') as f:
        for package in packages:
                f.write("{}\n".format(package))
    print('done!')
    sys.stdout.flush()

def main():
    parser = argparse.ArgumentParser(\
            prog='pip-cache', \
            description='Handle an offline cache of available pip libraries')
    subparsers = parser.add_subparsers()

    parser_update = subparsers.add_parser('update', \
            help='Updates the local cache of pip package names')
    parser_update.set_defaults(func=update_package_list)

    parser_pkgnames = subparsers.add_parser('pkgnames', \
            help='List packages whose names start with a prefix')
    parser_pkgnames.add_argument('prefix', type=str, help='Optional prefix.', \
            default='')
    parser_pkgnames.set_defaults(func=pkgnames)
    #args = parser.parse_args(['pkgnames', 'test'])
    #args = parser.parse_args(['update'])
    args = parser.parse_args(sys.argv[1:])
    func_args = vars(args)
    func_args = dict(func_args)
    func_args.pop('func', None)
    args.func(**func_args)

if __name__ == '__main__':
    main()
