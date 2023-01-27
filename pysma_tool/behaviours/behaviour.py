from abc import ABC, abstractclassmethod
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..agent import Agent


class Behaviour(ABC):

    def __init__(self) -> None:
        super().__init__()
        self._agent: Optional["Agent"] = None
        self._already_start: bool = False

    @property
    def agent(self) -> "Agent":
        return self._agent

    @agent.setter
    def agent(self, agent: "Agent") -> None:
        self._agent = agent

    @property
    def already_start(self) -> bool:
        return self._already_start

    @already_start.setter
    def already_start(self, already_start: bool) -> None:
        self._already_start = already_start

    @abstractclassmethod
    def action(self) -> None:
        """Set operations to be performed by the behavior. 
        
        To be implemented...
        """
        pass

    @abstractclassmethod
    def done(self) -> bool:
        """Get the behaviour has completed its execution.

        To be implemented...
        
        Returns:
            bool: True if the behaviour has completed its execution."""
        pass

    def on_start(self) -> None:
        """Call before action method."""
        pass

    def on_end(self) -> int:
        """Call after done method.

        Returns:
            int: Code to finish behaviour. By default 0.
        """
        return 0
