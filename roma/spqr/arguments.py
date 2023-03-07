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
# ====-==================================================================-======
"""TODO: add description here (v1.0.0.dev5)"""

from .censor import check_type
from collections import OrderedDict

import re


class Arguments(object):
  """TODO: description (v1.0.0.dev5)"""

  def __init__(self, name: str, *args, **kwargs):
    self.func_name = check_type(name, str)
    self.arg_list = args
    self.arg_dict = OrderedDict(kwargs)


  def __str__(self):
    return '{}({})'.format(self.func_name, ', '.join(
      list(self.arg_list) +
      ['{}={}'.format(k, v) for k, v in self.arg_dict.items()]))


  @staticmethod
  def parse(arg_string: str):
    """Parse arg_string and return an instance of Arguments.

    The format of arg_string should be:
    'entry_name arg1 ... argN kwarg1=v1 ... kwargM=vM'

    The best usage of this method is parsing the arguments for a specific
    python method. For example, given a method

        def add(x, y, shift=0):
          return x + y + shift

    and a command line argument string

        arg_string = 'add 12 19 shift=316'

    We have

        a = Arguments.parse(arg_string)
        assert add(*a.arg_list, **a.arg_dict) == 347

    :param arg_string: argument string in a given format above
    :return: an instance of Arguments
    """
    check_type(arg_string, str)
    pieces = arg_string.split(' ')
    assert len(pieces) > 0

    # (1) func_name
    func_name = pieces.pop(0)
    r = re.match(r'^[a-z_]+\w+$', func_name)
    if r is None: raise ValueError(
      "function name '{}' is illegal.".format(func_name))

    # (2) arg_list
    args = []
    while len(pieces) > 0 and '=' not in pieces[0]:
      args.append(pieces.pop(0))

    # (3) arg_dict
    kwargs = OrderedDict()
    while len(pieces) > 0:
      piece = pieces.pop(0)
      r = re.match(r'(^[a-zA-Z0-9_]+)=(.+)', piece)
      if r is None or len(r.groups()) != 2: raise ValueError(
        "Illegal string for kwargs: " + piece)
      k, v =  r.groups()
      kwargs[k] = v

    return Arguments(func_name, *args, **kwargs)

