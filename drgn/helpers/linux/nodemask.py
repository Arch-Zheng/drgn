# Copyright (c) ByteDance, Inc. and its affiliates.
# SPDX-License-Identifier: GPL-3.0-or-later

"""
NUMA Node Masks
---------

The ``drgn.helpers.linux.nodemask`` module provides helpers for working with
NUMA Node masks from :linux:`include/linux/nodemask.h`.
"""

from typing import Iterator

from drgn import Object, Program, sizeof, IntegerLike
from drgn.helpers.linux.cpumask import _for_each_set_bit

__all__ = (
    "for_each_node",
    "for_each_online_node",
    "for_each_node_state",
    "for_each_node_mask",
)

def for_each_node_mask(mask: Object) -> Iterator[int]:
    """
    Iterate over all of the NUMA nodes in the given mask.

    :param mask: ``nodemask_t``
    """
    try:
        nr_node_ids = mask.prog_["nr_node_ids"].value_()
    except KeyError:
        nr_node_ids = 1
    return _for_each_set_bit(mask.bits, nr_node_ids)

def for_each_node_state(prog: Program, state: IntegerLike) -> Iterator[int]:
    """
        Iterate over all NUMA nodes in the given state.

        :param state: ``enum node_states`` (e.g., ``N_NORMAL_MEMORY``).
    """
    mask = prog['node_states'][state]
    return for_each_node_mask(mask)

def for_each_node(prog: Program) -> Iterator[int]:
    """Iterate over all possible NUMA nodes."""
    return for_each_node_state(prog, prog["N_POSSIBLE"])

def for_each_online_node(prog: Program) -> Iterator[int]:
    """Iterate over all online NUMA nodes."""
    return for_each_node_state(prog, prog["N_ONLINE"])
