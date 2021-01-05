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
# ==============================================================================
"""This module defines basic class for build-functions"""

from ...spqr.censor import check_type
from .. import city


class Scroll(object):

  names = []

  def __init__(self, city_):
    self.city = check_type(city_, city.City)


  def __call__(self, *args, **kwargs):
    raise NotImplementedError


  def register(self, func_dict):
    check_type(func_dict, dict)
    assert len(self.names) > 0
    for name in self.names: func_dict[name] = self
