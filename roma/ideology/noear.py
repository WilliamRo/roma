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
# ==-========================================================================-==
from collections import OrderedDict


class Nomear(object):
  """This class is designed to provide a `pocket` dictionary for instances
  of classes inherited from it. If you are curious about its name, append
  `od` and reverse. One of the cool things about this class is that users
  do not need to call its constructor/initializer.

  This class follows the coding philosophy that some fields of a certain
  class do not need to be explicitly appear in constructor. Sometimes put
  them into a pocket is more comfortable.
  """

  _LOCAL_POCKET_KEY = '_LOCAL_POCKET'

  _register = OrderedDict()


  @property
  def _pocket(self) -> OrderedDict:
    if hasattr(self, self._LOCAL_POCKET_KEY):
      return getattr(self, self._LOCAL_POCKET_KEY)

    # If self is not registered, register
    if self not in self._register: self._register[self] = OrderedDict()
    return self._register[self]


  def localize(self):
    """Localize self._pocket so that stuff inside can be saved to disk"""
    setattr(self, self._LOCAL_POCKET_KEY, self._pocket)


  def get_from_pocket(self, key: str, default=None, initializer=None):
    if key not in self._pocket:
      if callable(initializer): self._pocket[key] = initializer()
      else: return default
    return self._pocket[key]


  def put_into_pocket(self, key: str, thing, exclusive=True):
    if key in self._pocket and exclusive:
      raise KeyError("`{}` already exists in {}'s pocket.".format(key, self))
    self._pocket[key] = thing


  def replace_stuff(self, key: str, val):
    assert key in self._pocket
    self._pocket[key] = val


  def __getitem__(self, item):
    return self.get_from_pocket(item)


  def __setitem__(self, key, value):
    self.put_into_pocket(key, value)
