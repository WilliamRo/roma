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

  _LOCAL_POCKET_KEY = '_NOMEAR_LOCAL_POCKET'

  cloud = OrderedDict()


  @property
  def _cloud_pocket(self) -> OrderedDict:
    # Register self in Nomear cloud if necessary
    if self not in self.cloud: self.cloud[self] = OrderedDict()
    return self.cloud[self]


  @property
  def _local_pocket(self) -> OrderedDict:
    # Initialize local pocket if necessary
    if not hasattr(self, self._LOCAL_POCKET_KEY):
      setattr(self, self._LOCAL_POCKET_KEY, OrderedDict())
    return getattr(self, self._LOCAL_POCKET_KEY)


  @property
  def _pocket(self) -> OrderedDict:
    p = self._cloud_pocket.copy()
    p.update(self._local_pocket)
    return p


  def in_pocket(self, key):
    return key in self._pocket


  def localize(self, key, exclusive=False, key_should_exist=False):
    if key not in self._cloud_pocket:
      if key_should_exist: raise KeyError(
        "!! `{}` not found in {}'s cloud pocket.".format(key, self))
      else: return None

    return self.put_into_pocket(
      key, self._cloud_pocket[key], exclusive, local=True)


  def get_from_pocket(
      self, key: str, default=None, initializer=None, local=False,
      key_should_exist=False):
    if not self.in_pocket(key):
      if callable(initializer):
        return self.put_into_pocket(key, initializer(), local=local)
      elif key_should_exist: raise KeyError(
        "!! `{}` not found in {}'s pockets.".format(key, self))
      else: return default
    return self._pocket[key]


  def put_into_pocket(self, key: str, thing, exclusive=True, local=False):
    pocket = self._local_pocket if local else self._cloud_pocket
    if key in pocket and exclusive: raise KeyError(
      "`{}` already exists in {}'s {} pocket.".format(
        key, self, 'local' if local else 'cloud'))
    pocket[key] = thing
    return thing


  def replace_stuff(self, key: str, val, local=False):
    pocket = self._local_pocket if local else self._cloud_pocket
    assert key in pocket
    pocket[key] = val


  def __getitem__(self, item):
    return self.get_from_pocket(item, key_should_exist=True)


  def __setitem__(self, key, value):
    self.put_into_pocket(key, value)
