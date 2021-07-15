# Copyright (c) ByteDance, Inc. and its affiliates.
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

from drgn.helpers.linux.nodemask import (
    for_each_node,
    for_each_online_node,
)
from tests.helpers.linux import LinuxHelperTestCase

NODE_PATH = Path("/sys/devices/system/node")

def parse_nodelist(nodelist):
    nodes = set()
    for node_range in nodelist.split(","):
        first, sep, last = node_range.partition("-")
        if sep:
            nodes.update(range(int(first), int(last) + 1))
        else:
            nodes.add(int(first))
    return nodes

class TestNodeMask(LinuxHelperTestCase):
    def _test_for_each_node(self, func, name):
        self.assertEqual(
            list(func(self.prog)),
            sorted(parse_nodelist((NODE_PATH / name).read_text())),
        )

    def test_for_each_node(self):
        self._test_for_each_node(for_each_node, "possible")

    def test_for_each_online_node(self):
        self._test_for_each_node(for_each_online_node, "online")
