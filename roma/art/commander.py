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
# ====-=============================================================-===========
from ..console.console import console
from ..ideology.noear import Nomear
from .tkutils.simple_dialogs import ask_string
from .tipbox import TipBox

import inspect
import tkinter as tk
import traceback



class Commander(Nomear):

  # region: Properties

  @Nomear.property()
  def command_history(self) -> list: return []

  @property
  def on_command_text_changed(self):
    """A method for responding to text-changed events in the asking dialog.
    This method should accept 2 arguments:
     (1) changed_text: str; (2) root: tk.Root
    """
    return self.get_from_pocket('on_command_text_changed', default=None)

  @on_command_text_changed.setter
  def on_command_text_changed(self, func):
    assert callable(func)
    self.put_into_pocket('on_command_text_changed', func)

  @Nomear.property()
  def command_hints(self) -> dict: return {}

  _SECRETARY_KEY = 'SeCReTArY'

  @property
  def secretary(self) -> TipBox:
    return self.get_from_pocket(self._SECRETARY_KEY, default=None)

  # endregion: Properties

  # region: Public Methods

  def default_on_command_text_changed(self, text, root):
    assert isinstance(text, str) and isinstance(root, tk.Tk)

    # Get the TipBox
    secretary: TipBox = self.get_from_pocket(
      self._SECRETARY_KEY, initializer=lambda: TipBox())

    # Get func name, hide tip if func_name is not ready
    func_name = text.split(' ')[0]
    if len(func_name) < 2:
      secretary.hide()
      return

    # Set message according to func_name
    func = self._get_attribute(func_name, None)
    if func is None:
      msg = f'Command `{func_name}` not found'
    else:
      params = inspect.signature(func).parameters
      msg = f'{func_name}({", ".join([str(v) for v in params.values()])})'
      if func_name in self.command_hints:
        ch = self.command_hints[func_name]
        msg += '\n\n' + (ch() if callable(ch) else ch)
      elif func.__doc__: msg += '\n\n' + func.__doc__

    secretary.set_message(msg)
    secretary.show()

    # Set location
    entry = root.winfo_children()[0]
    x, y = entry.winfo_rootx(), entry.winfo_rooty() + entry.winfo_height() + 1
    secretary.geometry(f'+{x}+{y}')

  def call(self):
    cmd = self.ask(history_buffer=self.command_history,
                   on_command_text_changed=self.on_command_text_changed)
    # Quit secretary if exists
    if self.secretary is not None: self.secretary.hide()
    if cmd is None: return
    cmd_string, func_key, args, kwargs = cmd

    # Add cmd_string to history buffer anyway
    self.command_history.insert(0, cmd_string)

    # Get method
    func = self._get_attribute(func_key, None)
    if not callable(func):
      self._err(' ! command `{}` not found.'.format(func_key))
      return

    # Try to execute func
    params_dict = inspect.signature(func).parameters
    params_values = list(params_dict.values())
    has_annotation = lambda p: p.annotation is not inspect._empty
    try:
      # Try to convert args type
      for i in range(len(args)):
        p = params_values[i]
        if has_annotation(p): args[i] = p.annotation(args[i])
      # Try to convert kwargs type
      for k, v in kwargs.items():
        p = params_dict[k]
        if has_annotation(p): kwargs[k] = p.annotation(v)

      # Execute
      func(*args, **kwargs)
    except:
      self._err(' ! Failed to execute command `{}`'.format(cmd_string))
      self._err('.. Error Message:')
      self._err('- ' * 39)
      self._err(traceback.format_exc() + '- ' * 39)


  @staticmethod
  def ask(history_buffer=(), on_command_text_changed=None):
    # Ask for command
    s = ask_string(history_buffer=history_buffer,
                   on_text_changed=on_command_text_changed)
    if s is None: return None

    assert isinstance(s, str)
    parts = s.split(' ')
    assert len(parts) > 0

    # Parse string
    func_key, args, kwargs, flag = parts.pop(0), [], {}, True
    for p in parts:
      if '=' in p:
        _p = p.split('=')
        if len(_p) != 2:
          flag = False
          break
        kwargs[_p[0]] = _p[1]
      else: args.append(p)

    # Check and return
    if not flag:
      Commander._err(' ! `{}` is not an appropriate command'.format(s))
      return None
    return s, func_key, args, kwargs

  # endregion: Public Methods

  # region: Private Methods

  def _get_attribute(self, key, default_value):
    return getattr(self, key, default_value)

  @staticmethod
  def _err(text):
    console.write_line(text, color='red')

  # endregion: Private Methods
