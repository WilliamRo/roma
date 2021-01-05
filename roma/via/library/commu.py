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
"""Build-in functions for communication"""

from ...console.console import console
from .scroll import Scroll

import socket


class SendMsg(Scroll):

  names = ['sendmsg', 'send_msg']

  def __call__(self, ip, port, msg):
    s = self.city.socket
    assert isinstance(s, socket.socket)


    console.write_line("Sending '{}' to {}:{} ...".format(msg, ip, port))
    return False


