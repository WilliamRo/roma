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
# =-=========================================================================-=
"""This module is originally from the `tframe` package.

Example:

    table = Table(12, 9, 8, 8, 7, tab=tab, margin=margin, buffered=True)
    table.specify_format(
      None, *(['{:.' + str(decimal) + 'f}'] * 3), None, align='lrrrr')
    table.print_header('', 'Precision', 'Recall', 'F1-Score', 'Support')

    # Show performance detail for each class
    if class_details:
      for i, name in enumerate(names):
        table.print_row(name, self.precisions[i], self.recalls[i],
                        self.F1s[i], self.support[i])
      table.hline()

    # Show overall performance
    table.print_row('Accuracy', '', '', self.accuracy, self.total)
    table.print_row('Macro Avg', self.macro_precision, self.macro_recall,
                    self.macro_F1, self.total)
    table.print_row('Weighted Avg', self.weighted_precision,
                    self.weighted_recall, self.weighted_F1, self.total)
    table.hline()


Result:

      ------------------------------------------------------
                      Precision   Recall  F1-Score  Support
      ======================================================
       Goose              0.308    0.667    0.421         6
       Cat                0.667    0.200    0.308        10
       Dog                0.667    0.667    0.667         9
      ------------------------------------------------------
       Accuracy                             0.480        25
       Macro Avg          0.547    0.511    0.465        25
       Weighted Avg       0.581    0.480    0.464        25
      ------------------------------------------------------
"""



class Table(object):

  def __init__(self, *widths, tab=4, margin=2, buffered=False, indent=0):
    assert len(widths) > 0
    self.columns = len(widths)
    self._widths = widths
    self._margin = margin
    self._tab = tab
    self._col_fmt = ['{}'] * self.columns
    self._align = None
    self._buffered = buffered
    self._buffer = []
    self._indent = indent

  @property
  def content(self): return '\n'.join(self._buffer)

  @property
  def tab(self): return ' ' * self._tab

  @property
  def hline_width(self):
    return sum(self._widths) + self._tab * (self.columns - 1) + 2 * self._margin

  def __str__(self): return self.content

  def print(self, string):
    indentation = ' ' * self._indent
    if self._buffered: self._buffer.append(indentation + string)
    else: print(indentation + string)

  def hline(self): self.print('-' * self.hline_width)

  def hdash(self): self.print('- ' * int(self.hline_width / 2))

  def dhline(self): self.print('=' * self.hline_width)

  def specify_format(self, *fmts, align=None):
    if len(fmts) == 0: fmts = [None] * self.columns
    assert len(fmts) == self.columns
    self._col_fmt = ['{}' if f in (None, '') else f for f in fmts]
    if align is not None:
      self._align = align
      assert len(align) == self.columns

  def _get_line(self, cells):
    if self._align is None: return self.tab.join(
      [(('{:>' if i > 0 else '{:<') + str(w) + '}').format(c[:w])
       for i, (c, w) in enumerate(zip(cells, self._widths))])
    else: return self.tab.join(
      [(('{:>' if a == 'r' else '{:<') + str(w) + '}').format(c[:w])
       for c, w, a in zip(cells, self._widths, self._align)])

  def print_with_margin(self, content):
    margin = ' ' * self._margin
    self.print('{0}{1}{0}'.format(margin, content))

  def print_header(self, *header, hline=True):
    if hline: self.hline()
    self.print_row(*header)
    if hline: self.dhline()

  def print_row(self, *cells):
    assert len(cells) == self.columns
    cells = [c if isinstance(c, str) else fmt.format(c)
             for c, fmt in zip(cells, self._col_fmt)]
    self.print_with_margin(self._get_line(cells))

  def print_buffer(self, indent=0):
    for row in self._buffer: print('{}{}'.format(' ' * indent, row))

