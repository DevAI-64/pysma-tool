"""Behaviour status enum module"""

from enum import Enum


class BehaviourStatus(Enum):
    """Define status of Behaviour."""

    NOT_STARTED = 0
    STARTED = 1
    BLOCKED = 2
    STOPPED = 3
