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
# ====-==============================================================-==========
"""This module provides methods related to types of method arguments.
"""
from ..spqr import atticus


def check_type(input_, type_=None, inner_type=None, nullable=False,
               auto_conversion=True):
  """Check the type of the given inputs. This method can also be used as a
  parser for converting strings to numbers.

  When type_ is a groups of more than 1 types, auto conversion will not be
  performed even when auto_conversion is True.

  When input_ is a large group, calling this method frequently may bring
  time overhead which is not neglectable since it involves process to build
  a list of the same scale as the input group.

  Examples:
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  >>> check_type(31, int)
  31

  >>> check_type({'adh', 93, 19}, inner_type=str)
  {None, 93, 19}

  >>> check_type([None, 12, 19.0], tuple, inner_type=int, nullable=True)
  (None, 12, 19),
  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

  :param input_: input to be checked
  :param type_: a type or tuple/list/set of types, None by default.
                When this arg is None, inner_type must be specified and
                input_ is assumed to be in group types.
  :param inner_type: if specified, arg type_ must be None or one of group_types
  :param nullable: case 1: inner_type is None: whether input_ can be None
                   case 2: inner_type is not None: whether value in input_
                           can be None
  :param auto_conversion: whether to perform automatic type conversion.
                          Works only when arg 2 is a type.
  :return: input_, may be converted
  """
  group_types = (tuple, list, set)

  # Sanity check
  if all([type_ is None, inner_type is None]): raise ValueError(
      '!! check_type() arg 2 and 3 can not be None at the same time')

  # Check nullable (logically this line is not necessary)
  if all([nullable, input_ is None, inner_type is None]): return None

  # Make sure type_/inner_type is legal for isinstance() arg 2.
  # After this code block, type_/inner_type will be a type or a tuple of at
  # least 2 types
  def _check_type_type(_type, arg_ind):
    assert arg_ind in (2, 3)
    if _type is None: return None
    if isinstance(_type, group_types):
      type_is_legal = all([isinstance(t, type) for t in _type])
      _type = tuple(_type) if len(_type) > 1 else _type[0]
    else: type_is_legal = isinstance(_type, type)
    if not type_is_legal: raise TypeError(
      '!! check_type() arg {} must be a type or tuple/list/set of types'.format(
        arg_ind))
    return _type

  type_ = _check_type_type(type_, 2)
  inner_type = _check_type_type(inner_type, 3)

  # Define some inner methods for checking input_
  def _safe_convert(src, tgt_type):
    tgt = tgt_type(src)
    if all([isinstance(src, float), isinstance(tgt, int), src != tgt]):
      raise ValueError('!! Failed to convert {} to integer.'.format(src))
    return tgt

  def _raise_error(val, name, _type, convert=False):
    msg = '!! {0} (value: {1}) does not match{3} the required type {2}.'.format(
      name, val, _type, ' and can not be converted to' if convert else '')
    raise TypeError(msg)

  def _check_type(inp, _type, name='check_type() arg 1'):
    if not isinstance(inp, _type):
      if nullable and inp is None: return None
      if isinstance(_type, type) and auto_conversion:
        try: return _safe_convert(inp, _type)
        except: _raise_error(inp, name, _type, convert=True)
      _raise_error(inp, name, _type, convert=False)
    return inp

  # Check input_
  if type_ is None: type_ = group_types
  input_ = _check_type(input_, type_)
  if inner_type is None: return input_
  # Make sure input is a group
  assert inner_type is not None and isinstance(input_, group_types)
  return type(input_)(
    [_check_type(inp, inner_type, 'The {} element of check_type() arg 1'.format(
      atticus.ordinal(i + 1))) for i, inp in enumerate(input_)])


if __name__ == '__main__':
  assert all([
    check_type(31, int) == 31,
    check_type({'adh', 93, 19}, inner_type=str) == {'adh', '93', '19'},
    check_type([None, 12, 19.0], tuple,
               inner_type=int, nullable=True) == (None, 12, 19),
  ])
