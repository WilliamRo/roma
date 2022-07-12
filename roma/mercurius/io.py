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
# ==-==========================================================================-
from roma import console

import pickle
import os



def dir_and_fn(file_path: str):
  return os.path.dirname(file_path), os.path.basename(file_path)



def load_file(file_path: str, verbose: bool = False):
  if verbose:
    dn, fn = dir_and_fn(file_path)
    console.show_status(f'Loading `{fn}` from `{dn}` ...')
  with open(file_path, 'rb') as file: return pickle.load(file)



def save_file(obj, file_path: str, verbose: bool = False):
  dn, fn = dir_and_fn(file_path)
  if verbose: console.show_status(f'Saving `{fn}` to `{dn}` ...')
  with open(file_path, 'wb') as output:
    pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
  if verbose: console.show_status(f'`{fn}` has been saved to `{dn}`.')
