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
# =-==========================================================================-
import time

from roma import Nomear
from typing import Callable

import threading



class XNode(Nomear):

  KEY_SHOULD_TERMINATE = 'KEY_SHOULD_TERMINATE'
  KEY_PARENT_THREAD = 'KEY_PARENT_THREAD'

  @property
  def parent_node(self):
    return self.get_from_pocket(self.KEY_PARENT_THREAD, key_should_exist=True)


  @parent_node.setter
  def parent_node(self, val):
    assert isinstance(val, XNode)
    self.put_into_pocket(self.KEY_PARENT_THREAD, val)


  @Nomear.property()
  def child_nodes(self): return []


  @property
  def should_terminate(self):
    # Otherwise, check the corresponding flag in pocket
    return self.get_from_pocket(self.KEY_SHOULD_TERMINATE, False)


  @Nomear.property(key='this_thread')
  def thread(self):
    return threading.currentThread()


  def terminate(self, block=False):
    """Terminate this thread, which should be executed as long-live thread.
    """
    self.put_into_pocket(self.KEY_SHOULD_TERMINATE, True, exclusive=False)
    assert isinstance(self.parent_node, XNode)
    self.parent_node.child_nodes.remove(self)
    if block: self.thread.join()


  def execute_a_new_child(self, func: Callable, long_live: bool = True,
                          daemon: bool = True):
    """Life cycle of children executed using this method will follow &self
    """
    node = XNode()
    self.child_nodes.append(node)
    node.parent_node = self
    node.execute_async(func, long_live, daemon=daemon)
    return node


  def execute_async(self, func: Callable, long_live: bool = True,
                    daemon: bool = True):
    if long_live: func = self._get_while_loop(func)
    t = threading.Thread(target=func, daemon=daemon)
    self.put_into_pocket('this_thread', t)
    t.start()


  def _get_while_loop(self, func: Callable):
    def while_loop():
      while not self.should_terminate:
        func()
    return while_loop


