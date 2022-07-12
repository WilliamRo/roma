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
"""City hall"""

from ..spqr.arguments import Arguments
from ..spqr.censor import check_type
from ..console.console import console

from . import city
from . import library


class Hall(object):

  def __init__(self, city_, **funcs):
    self.city = check_type(city_, city.City)
    self.funcs = funcs
    # Register build-in functions
    library.register(city_, self.funcs)


  def handle(self, cmd):
    # Parse command
    a = Arguments.parse(cmd)
    if a.func_name not in self.funcs:
      console.show_status(
        "Unknown command '{}'".format(a.func_name), prompt='!!', color='red')
      return False
    return self.funcs[a.func_name](*a.arg_list, **a.arg_dict)

