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
from .misc import center

import tkinter as tk



def ask_string(history_buffer=(), on_text_changed=None):
  """This widget works like pressing `:` in IdeaVim.

     history_buffer = [latest_cmd, ...]
  """
  # Insert current input into history buffer
  history_buffer = [''] + list(history_buffer)

  # box[0]: string to return
  # box[1]: history cursor
  # box[2]: allow to trigger text changed event
  box = [None, 0, True]

  root = tk.Tk()
  root.title('')
  root.resizable(0, 0)

  # Create text box and string var
  sv = tk.StringVar(root)
  def _text_modified():
    if box[-1]: history_buffer[0] = sv.get()
    if callable(on_text_changed): on_text_changed(sv.get(), root)
  sv.trace_add('write', lambda *args: _text_modified())
  text_box = tk.Entry(root, width=50, textvariable=sv)
  text_box.pack()
  text_box.focus()

  # Bind events
  def _close(coin: bool):
    if coin: box[0] = text_box.get()
    root.destroy()
    # this line is necessary, otherwise msg will not be delivered immediately
    root.quit()

  def _fill_in_history(d):
    if not history_buffer: return
    assert d in (-1, 1)

    # Find cursor
    cursor = max(min((box[1] + d), len(history_buffer) - 1), 0)
    if cursor == box[1]: return

    # Update
    text_to_fill = history_buffer[cursor]
    box[1] = cursor

    # Fill (avoid triggering text changed event)
    box[-1] = False
    text_box.delete(0, tk.END)
    text_box.insert(0, text_to_fill)
    box[-1] = True

  root.bind('<Return>', lambda _: _close(True))
  root.bind('<Escape>', lambda _: _close(False))
  root.bind('<Control-n>', lambda _: _fill_in_history(-1))
  root.bind('<Control-p>', lambda _: _fill_in_history(1))

  # Display dialog at the center
  center(root)
  root.focus_force()
  text_box.focus_set()  # Added on 2023-Jul-27 to fix focus issue in Win11
  root.mainloop()

  # Return the text in the text box
  return box[0]

