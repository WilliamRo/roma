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
# ===-=========================================================================-
"""This class manages all key shortcuts"""
from ..console.console import console
from ..ideology.noear import Nomear
from .frame import Frame
from typing import Callable, Union

import inspect
import tkinter as tk



class Shortcuts(Nomear):

  def __init__(self, easel: Frame):
    self.easel: Frame = easel
    # Library is a list of tuples, each tuple has two entries:
    # (1) callable functions (2) its description (3) color in manual
    self.library = {}

    # Bind key-press events
    self.easel.master.bind('<KeyPress>', self._on_key_press)

    # Register common events
    self._register_common_events()

  # region: Properties

  @property
  def root(self) -> tk.Tk:
    return self.easel.master

  # endregion: Properties

  # region: Public Methods

  def register_key_event(
      self, key_or_keys: Union[str, list, tuple], func: Callable,
      description: str, color='white', overwrite: bool = False):
    # If keys are provided
    if isinstance(key_or_keys, (tuple, list)):
      for key in key_or_keys:
        self.register_key_event(key, func, description, color, overwrite)
      return
    else: assert isinstance(key_or_keys, str)

    # Otherwise register a single key
    if key_or_keys in self.library and not overwrite:
      raise KeyError('!! Key `{}` has already been registered')
    assert callable(func)
    self.library[key_or_keys] = (func, description, color)

  def list_all_shortcuts(self):
    console.show_info('Shortcuts:')
    for key, (_, description, color) in self.library.items():
      console.supplement(f'{key}: {description}', color=color)

  # endregion: Public Methods

  # region: Events

  def _register_common_events(self):
    # Quit
    self.register_key_event(['q', 'escape'], lambda: self.root.destroy(),
                            description='Close window', color='blue')
    # Call commander
    self.register_key_event('colon', getattr(self.easel, 'call'),
                            description='Call commander', color='blue')

  def _on_key_press(self, event: tk.Event):
    key = getattr(event, 'keysym').lower()

    if key in self.library:
      func = self.library[key][0]
      # Call method with proper arguments
      kwargs = self._get_kwargs_for_event(func)
      func(**kwargs)
    elif key not in ('control_l', 'alt_l', 'shift_l'):
      # Ignore modifiers
      print('>> key "{}" pressed'.format(key))

  def _get_kwargs_for_event(self, func):
    """This method is inherited from DaVinci"""
    assert callable(func)
    # Get method signature
    sig = inspect.signature(func).parameters
    # Get key-word arguments for method according to its signature
    kwargs = {}
    for kw in sig.keys():
      if kw in ['easel']:
        kwargs[kw] = self.easel
      elif kw in ['root']:
        kwargs[kw] = self.root
    return kwargs

  # endregion: Events





