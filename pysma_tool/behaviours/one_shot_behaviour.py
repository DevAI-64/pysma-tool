"""One shot behaviour module"""

from .behaviour import Behaviour


class OneShotBehaviour(Behaviour):
    """Define one shot behaviour inherits Behaviour class."""

    def done(self) -> bool:
        """Get the behaviour has completed its execution.

        Returns:
            bool: True everytime.
        """
        return True
