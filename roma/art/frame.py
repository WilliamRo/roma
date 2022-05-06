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
# ====-======================================================================-==
"""This class can be viewed as an extension of ttk.Frame"""
from ..ideology.noear import Nomear
from .tkutils.misc import center
from tkinter import ttk

import tkinter as tk



class Frame(ttk.Frame, Nomear):

  def __init__(self, master=None):
    # If master is not provided, load a default one
    if master is None: master = tk.Tk()
    # Call ttk.Frame's constructor
    super(Frame, self).__init__(master=master)

  # region: Public Methods

  def show(self, show_in_center=True):
    self.refresh()
    if show_in_center:
      assert isinstance(self.master, tk.Tk)
      center(self.master)
    self.master.mainloop()

  def refresh(self): pass

  # endregion: Public Methods



if __name__ == '__main__':
  frame = Frame()
  frame.show()

