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
# =-===========================================================================-
"""An easel holds the canvas."""
from .frame import Frame
from .shortcuts import Shortcuts
from .tkutils.misc import center
from collections import OrderedDict
from typing import Union, Optional
from roma.art.commander import Commander

import os
import tkinter as tk



class Easel(Commander, Frame):
  """An Easel has a layout of
  root (an instance of tk.Tk)
     |- Easel
           |- Frame1
           ...
           |- Widget1
           ...
  """

  def __init__(self):

    # Call parent's constructor. As the top frame, an Easel has no master Frame.
    super(Easel, self).__init__()
    self.window.withdraw()

    # An Easel has a shortcut, which is bound to root
    self.shortcuts = Shortcuts(easel=self)

  # region: Properties

  @property
  def window(self) -> tk.Tk: return self.master

  @property
  def title(self) -> str: return self.window.wm_title()

  @title.setter
  def title(self, text): self.window.wm_title(text)

  @Frame.property()
  def axes(self): return OrderedDict()

  @Frame.property()
  def cursors(self): return OrderedDict()

  @property
  def cursor_string(self):
    return ''.join([
      f'[{self.cursors[key] + 1}/{len(values)}]'
      for key, values in self.axes.items() if len(values) > 1])

  # endregion: Properties

  # region: Private Methods

  def _set_style(self):
    default_ico = os.path.join(
      os.path.dirname(os.path.abspath(__file__)), 'resources\goose64.ico')
    self.window.wm_iconbitmap(default_ico)

  def _check_axis_key(self, key, should_exist=True):
    if should_exist and key not in self.axes:
      raise KeyError(f'!! axes `{key}` not found')
    elif not should_exist and key in self.axes:
      raise KeyError(f'!! axes `{key}` already exists')

  # endregion: Private Methods

  # region: Public Methods

  def add_to_axis(self, key: str, value, index=-1):
    self._check_axis_key(key)
    # Convert tuple to list if necessary
    if isinstance(self.axes[key], tuple):
      self.axes[key] = list(self.axes[key])
    if index == -1: self.axes[key].append(value)
    else: self.axes[key].insert(index, value)

  def set_to_axis(self, key: str, value: Union[tuple, list], overwrite=False):
    if not overwrite: self._check_axis_key(key, should_exist=False)
    self.axes[key] = value
    self.cursors[key] = 0

  def create_dimension(self, key): self.set_to_axis(key, [])

  def set_cursor(self, key: str, step: int = 0, cursor: Optional[int] = None,
                 refresh: bool = False):
    self._check_axis_key(key)
    if len(self.axes[key]) < 2: return
    previous_cursor = self.cursors[key]
    if cursor is None: cursor = previous_cursor + step
    self.cursors[key] = cursor % len(self.axes[key])
    # Refresh easel if necessary
    if refresh and self.cursors[key] != previous_cursor: self.refresh()

  def get_element(self, key: str):
    self._check_axis_key(key)
    if len(self.axes[key]) == 0: return None
    return self.axes[key][self.cursors[key]]

  def show(self, show_in_center=True):
    self.refresh()
    self.window.deiconify()
    if show_in_center:
      assert isinstance(self.window, tk.Tk)
      center(self.window)

    # Set style after mainloop, other a window may appear before mainloop
    delay_ms = 20
    self.window.after(delay_ms, self._set_style)
    self.window.after(delay_ms, self.window.focus_force)

    # Begin mainloop
    self.window.mainloop()

  # endregion: Public Methods

  # region: Builtin Commands

  def man(self): self.shortcuts.list_all_shortcuts()

  # endregion: Builtin Commands

