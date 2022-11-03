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
# ==-=======================================================================-===
import tkinter as tk



SHOW_DELAY_MS = 20


def center(window: tk.Tk):
  # Added by @Even to ensure windows are centered in Win11
  window.update_idletasks()

  h, w = window.winfo_reqheight(), window.winfo_reqwidth()
  H, W = window.winfo_screenheight(), window.winfo_screenwidth()
  x, y = (W - w) // 2, (H - h) // 2
  window.geometry("+{}+{}".format(x, y))


def show_elegantly(window: tk.Tk, show_in_center: bool = True):
  """This method is inherited from tframe.main_frame.show.
  Directly call `center` before calling mainloop somehow leads to an
  obvious flash of original window in some case. Thus window.after is
  used to abbreviate this phenomenon.
  """
  def init():
    if show_in_center: center(window)
    window.focus_force()
  window.after(SHOW_DELAY_MS, init)
  window.mainloop()



if __name__ == '__main__':
  root = tk.Tk()
  root.bind('q', lambda _: root.destroy())
  # show_elegantly(root)
  center(root)
  root.mainloop()


