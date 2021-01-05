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
# ====-========================================================================-
"""Build-in functions for a city is maintained in this package"""

from .scroll import Scroll

from .basic import ExitHall
from .commu import SendMsg

from .. import city


CONTENT = (
  ExitHall,
  SendMsg,
)


def register(city_, func_dict: dict):
  assert isinstance(city_, city.City)
  for s in CONTENT:
    assert issubclass(s, Scroll)
    s(city_).register(func_dict)


