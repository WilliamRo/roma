# Copyright 2020 William Ro. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ====-=====================================================================-==
"""This module provides methods for manipulating files"""
from ..console.console import console
from fnmatch import fnmatch

import os
import re
import zipfile


def walk(root_path, type_filter=None, pattern=None, ignored_patterns=(),
         re_pattern=None, return_basename=False, recursive=False,
         ignore_hidden_directories=True, include_folder_name=False) -> list:
  """Traverse through all files/folders under given `root_path`

  :param root_path: directory to be traversed
  :param type_filter: specify what type of path should be returned, can be
                      (1) None (default), indicating return all paths
                      (2) `file` for filtering out file paths
                      (3) `folder` or `dir` for filtering out directories
  :param pattern: patterns to be included using fnmatch
  :param ignored_patterns: patterns to be ignored using fnmatch
  :param re_pattern: patterns to be included using regular expression
  :param return_basename: whether to return the base name
  :param recursive: whether to traverse recursively.
                    If set to True, `return_basename` must be False
  :param ignore_hidden_directories: whether to ignore hidden directories
  :param include_folder_name: whether to include folder name when `type_filter`
                              is `file`. Designed for `tree` method
  :return: a list of paths
  """
  # Sanity check
  if not os.path.exists(root_path): raise FileNotFoundError(
    '!! Directory `{}` does not exist.'.format(root_path))

  # Get all paths under root_path
  paths = [os.path.join(root_path, p).replace('\\', '/')
           for p in os.listdir(root_path)]

  # Sort paths to avoid the inconsistency between Windows and Linux
  paths = sorted(paths)

  # Define filter function
  def filter_out(f, filter_full_path=False):
    if not callable(f): return paths
    _f = f if filter_full_path else lambda p: f(os.path.basename(p))
    return list(filter(_f, paths))

  # Filter path
  if type_filter in ('file', os.path.isfile):
    type_filter = os.path.isfile
  elif type_filter in ('folder', 'dir', os.path.isdir):
    type_filter = os.path.isdir
  elif type_filter is not None: raise ValueError(
    '!! `type_filter` should be one of (`file`, `folder`, `dir`)')
  paths = filter_out(type_filter, filter_full_path=True)

  # Include pattern using fnmatch if necessary
  if pattern is not None:
    paths = filter_out(lambda p: fnmatch(p, pattern))

  # Ignore patterns using fnmatch if necessary
  if isinstance(ignored_patterns, str): ignored_patterns = ignored_patterns,
  assert isinstance(ignored_patterns, (tuple, list))
  if ignore_hidden_directories:
    ignored_patterns = list(ignored_patterns) + ['.*']
  if len(ignored_patterns) > 0:
    paths = filter_out(
      lambda p: not any([fnmatch(p, ptn) for ptn in ignored_patterns]))

  # Filter pattern using regular expression if necessary
  if re_pattern is not None:
    paths = filter_out(lambda p: re.match(re_pattern, p) is not None)

  # Return if required
  if return_basename:
    if recursive: raise AssertionError(
      '!! Can not return base name when traversing recursively')
    return [os.path.basename(p) for p in paths]

  # Traverse sub-folders if required
  _walk = lambda p, t, r, ptn=None: walk(
    p, type_filter=t, pattern=ptn, re_pattern=re_pattern,
    ignored_patterns=ignored_patterns, return_basename=False, recursive=r,
    include_folder_name=include_folder_name)
  if recursive:
    for p in _walk(root_path, 'dir', False):
      # Walk into `p` first, if no targets found, skip
      sub_paths = _walk(p, type_filter, True, ptn=pattern)
      if len(sub_paths) == 0: continue

      if p in paths:
        paths.remove(p)
        paths.append(p)
      if p not in paths and include_folder_name:
        paths.append(p)
      paths.extend(sub_paths)
  return paths


def zip_dir(src_path, pattern, ignored_patterns=(), re_pattern=None,
            dst_path=None, overwrite=True, verbose=False,
            ignore_hidden_directories=True) -> str:
  """Create a ZIP file for all files with given pattern under `scr_path`

  :param src_path: source path
  :param pattern: patterns to be included using fnmatch
  :param ignored_patterns: patterns to be ignored using fnmatch
  :param re_pattern: patterns to be included using regular expression
  :param dst_path: directory to save .zip file
  :param overwrite: whether to overwrite if .zip file already exists
  :param verbose: whether or not to print processing details
  :param ignore_hidden_directories: whether to ignore hidden directories
  :return: path of the created .zip file
  """
  if verbose:
    console.show_status('Creating ZIP file for source directory:')
    console.split(color='yellow')
    tree(src_path, type_filter='file', pattern=pattern, re_pattern=re_pattern,
         ignored_patterns=ignored_patterns)
    console.split(color='yellow')

  # Check source path
  if not os.path.isdir(src_path):
    raise FileNotFoundError('!! Invalid directory `{}`.'.format(src_path))
  if src_path[-1] == '/': src_path = src_path[:-1]

  # Check destination path
  if dst_path is None: dst_path = src_path
  if os.path.isdir(dst_path):
    src_base_name = os.path.basename(src_path)
    dst_path = os.path.join(src_path, '{}.zip'.format(src_base_name))
  if not fnmatch(dst_path, '*.zip'):
    raise NameError('!! Illegal `dst_path`: {}'.format(dst_path))

  # Delete old zip file if exist
  if os.path.exists(src_path) and not overwrite:
    raise FileExistsError('!! ZIP file `{}` already exists.'.format(dst_path))

  # Create zip file
  file_paths = walk(src_path, type_filter='file', pattern=pattern,
                    re_pattern=re_pattern, ignored_patterns=ignored_patterns,
                    ignore_hidden_directories=ignore_hidden_directories,
                    recursive=True)
  with zipfile.ZipFile(dst_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    start = os.path.join(src_path, '..')
    for p in file_paths: zipf.write(p, os.path.relpath(p, start))

  # Finalize
  if verbose: console.show_status('ZIP file saved to `{}`.'.format(dst_path))
  return dst_path


def unzip_file(zip_path: str, dst_path: str, verbose=False):
  """Unzip a .zip file to `dst_path`

  :param zip_path: path of the .zip file to be unzipped
  :param dst_path: destination path
  :param verbose: whether to display processing details
  """
  if not zipfile.is_zipfile(zip_path):
    raise FileExistsError('!! Can not find ZIP file `{}`'.format(zip_path))

  with zipfile.ZipFile(zip_path, 'r') as zipf: zipf.extractall(dst_path)

  if verbose:
    console.show_status('`{}` unzipped to `{}`'.format(zip_path, dst_path))

  return dst_path


def tree(root_path: str, type_filter=None, pattern=None, ignored_patterns=(),
         re_pattern=None):
  """List a directory tree using walk. Example output:

  root_path
  |--foo.py
  |--sub-folder-1
  |--sub-folder-2
  |  |--sub-folder-2-1
  |     |--bar.py
  |- sub-folder-3

  :param root_path: directory to be traversed
  :param type_filter: specify what type of path should be returned, can be
                      (1) None (default), indicating return all paths
                      (2) `file` for filtering out file paths
                      (3) `folder` or `dir` for filtering out directories
  :param pattern: further filter out paths using fnmatch
  :param ignored_patterns: patterns to be ignored using fnmatch
  :param re_pattern: further filter out paths using regular expression
  """
  # Calculate root level
  if root_path[-1] == '/': root_path = root_path[:-1]
  level = lambda p: len(p.split('/'))
  root_level = level(root_path)
  get_prefix = lambda p: '|  ' * (level(p) - root_level - 1) + '|--'

  # Recursively get paths
  paths = walk(root_path=root_path, type_filter=type_filter, pattern=pattern,
               ignored_patterns=ignored_patterns, return_basename=False,
               re_pattern=re_pattern, recursive=True, include_folder_name=True)

  # Print tree
  console.write_line(console.fancify(root_path, 'bold'))
  for p in paths:
    prefix = console.fancify(get_prefix(p), 'white')
    name = os.path.basename(p)
    # Use bold font for directories
    if os.path.isdir(p): name = console.fancify(name, 'bold')
    console.write_line(prefix + name)


def synchronize(src_dir, dst_dir, pattern=None, ignored_patterns=(),
                re_pattern=None, ignore_hidden_directories=True, verbose=False):
  """Synchronize `dst_dir` with `src_dir`. This method was designed under the
  need of synchronizing the project directory on a GPU server with the local
  project directory which is hierarchical.

  :param src_dir: source directory
  :param dst_dir: destination directory
  :param pattern: patterns to be included using fnmatch
  :param ignored_patterns: patterns to be ignored using fnmatch
  :param re_pattern: patterns to be included using regular expression
  :param ignore_hidden_directories: whether to ignore hidden directories
  :param verbose: whether or not to print processing details
  """
  # Sanity check
  for path, name in zip((src_dir, dst_dir), ('Source', 'Destination')):
    if not os.path.exists(path): raise FileNotFoundError(
      '!! {} path `{}` not found.'.format(path, name))

  if os.path.basename(src_dir) != os.path.basename(dst_dir):
    raise AssertionError('!! Base name between source path `{}` and destination'
                         ' path `{}` should be the same.'.format(
      src_dir, dst_dir))

  # Create a .zip file from source path
  zip_path = zip_dir(src_dir, pattern, ignored_patterns, re_pattern,
                     ignore_hidden_directories=ignore_hidden_directories,
                     verbose=verbose)
  # Unzip
  unzip_file(zip_path, os.path.dirname(dst_dir), verbose=verbose)




