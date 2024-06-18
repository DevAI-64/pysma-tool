"""Parallel behaviour waiting method enum module"""

from enum import Enum


class ParallelBehaviourWaitingMethod(Enum):
    """Define waiting method of ParallelBehaviour."""

    WAIT_ALL = 0
    WAIT_ANY = 1
    WAIT_SELECTION = 2
