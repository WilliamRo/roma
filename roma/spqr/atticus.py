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
# ==-==========================================================================-
"""Titus Pomponius Atticus was a Roman editor who loved letters.
"""
from ..spqr import censor


def ordinal(n):
  """Convert a non-negative integer to its ordinal representation.

  :param n: a non-negative integer
  :return: the corresponding ordinal representation of input n
  """
  # Make sure n is a non-negative integer
  censor.check_type(n, int)
  # The terse solution below is taken from
  # http://golf.shinh.org/reveal.rb?1st%202nd%203rd%204th/xsot_1456205408&py
  return '{}{}'.format(n, 'tsnrhtdd'[n%5*(n%100^15>4>n%10)::4])


if __name__ == '__main__':
  for n in range(150): print(ordinal(n))

