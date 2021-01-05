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
"""City means node"""

from ..spqr import censor
from ..console.console import console
from . import hall

import socket


class City(object):
  """

  """

  def __init__(self, ip='', port=0, name='Roma', backlog=5, libs=None):
    """"""
    # Public attributes
    self.name = censor.check_type(name, str)

    # : Private attributes
    # Check libs and instantiate city hall
    if libs is None: libs = []
    elif isinstance(libs, str): libs = [libs]
    self._hall = hall.Hall(self, *censor.check_type(libs, inner_type=str))

    self._backlog = censor.check_type(backlog, int)

    # initiate a socket
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind socket
    self.socket.bind((ip, port))
    self._ip, self._port = self.socket.getsockname()
    console.show_status('City {} (located in {}) has been created.'.format(
      self.name, console.fancify(self.location_str, 'blue', 'underline')))


  # region: Properties

  @property
  def location(self):
    return self._ip, self._port

  @property
  def location_str(self):
    return '{}:{}'.format(self._ip, self._port)

  # endregion: Properties

  # region: Private Methods

  def _host(self):
    console.show_status('{} is hosting ...'.format(self.name))

  # endregion: Private Methods

  # region: Public Methods

  def enter_hall(self):
    """Enter the hall of this city"""
    console.show_status('Entered city hall.')
    while True:
      console.write('<= ', color='green')
      cmd = input()
      try:
        if self._hall.handle(cmd): return
      except Exception as e:
        console.show_status(
          'Fail to execute command \'{}\'. Error message:'.format(cmd),
          prompt='!!', color='red')
        console.supplement(e, color='red')

  # endregion: Public Methods

"""

    # Put this city on listen mode
    self._socket.listen(backlog)
"""



