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
from roma.art.commander import Commander
from .frame import Frame
from .shortcuts import Shortcuts

import tkinter as tk



class Easel(Commander, Frame):

  def __init__(self):

    # Call parent's constructor. As the top frame, an Easel has no master Frame.
    super(Easel, self).__init__()

    # An Easel has a shortcut
    self.shortcuts = Shortcuts(easel=self)

  # region: Properties

  @property
  def window(self) -> tk.Tk: return self.master

  @property
  def title(self) -> str: return self.window.wm_title()

  @title.setter
  def title(self, text): self.window.wm_title(text)


  # endregion: Properties

  # region: Public Methods


  # endregion: Public Methods

