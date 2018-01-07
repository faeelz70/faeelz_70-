#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_wishbone.py
#
#  Copyright 2017 Jelle Smet <development@smetj.net>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from wishbone.event import Event
from wishbone.module.fanout import Fanout
from wishbone.actor import ActorConfig
from wishbone.utils.test import getter


def test_module_fanout():

    actor_config = ActorConfig('fanout', 100, 1, {}, "", disable_exception_handling=True)
    fanout = Fanout(actor_config)
    fanout.pool.queue.inbox.disableFallThrough()

    fanout.pool.createQueue("one")
    fanout.pool.queue.one.disableFallThrough()

    fanout.pool.createQueue("two")
    fanout.pool.queue.two.disableFallThrough()

    fanout.start()

    e = Event(["hello"])

    fanout.pool.queue.inbox.put(e)
    one = getter(fanout.pool.queue.one)
    two = getter(fanout.pool.queue.two)

    fanout.stop()

    assert one.get() == ["hello"]
    assert two.get() == ["hello"]
    assert id(one.get()) != id(two.get())
