"""Cyclic behaviour module"""

from .behaviour import Behaviour


class CyclicBehaviour(Behaviour):
    """Define cyclic behaviour inherits Behaviour class."""

    def done(self) -> bool:
        """Get the behaviour has completed its execution.

        Returns:
            bool: False everytime.
        """
        return False
