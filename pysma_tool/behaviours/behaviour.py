"""Behaviour module."""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional, TYPE_CHECKING
from abc import ABC, abstractmethod

from .behaviour_status import BehaviourStatus

if TYPE_CHECKING:
    from ..agent import Agent
    from .composite_behaviour import CompositeBehaviour


class Behaviour(ABC):
    """Define Behaviour class.

    Attributes:
        agent (Optional[Agent]): Owner of the behaviour. By default is None.
        data_store (Dict[str, Any]): Data store of the behaviour. By default
            is empty.
        date_to_restart (Optional[datetime]): Date to restart a blocked
            behaviour. By default is None.
        init_state (Dict[str, Any]): Backup of initial state of the behaviour.
            By default is empty.
        name (str): The name of behaviour. By default is empty.
        status (BehaviourStatus): Status of behaviour. By default is
            NOT_STARTED.
        parent (Optional[CompositeBehaviour]): Parent of the behaviour. By
            default is None.
    """

    def __init__(self) -> None:
        """Instantiate Behaviour class."""
        self._agent: Optional["Agent"] = None
        self._data_store: Dict[str, Any] = {}
        self._date_to_restart: Optional[datetime] = None
        self._init_state: Dict[str, Any] = {}
        self._name: str = ""
        self._status: BehaviourStatus = BehaviourStatus.NOT_STARTED
        self._parent: Optional["CompositeBehaviour"] = None

    @property
    def agent(self) -> Optional["Agent"]:
        """Owner of the behaviour."""
        return self._agent

    @agent.setter
    def agent(self, agent: Optional["Agent"]) -> None:
        self._agent = agent

    @property
    def parent(self) -> Optional["CompositeBehaviour"]:
        """Parent of the behaviour."""
        return self._parent

    @parent.setter
    def parent(self, parent: Optional["CompositeBehaviour"]) -> None:
        self._parent = parent

    @property
    def status(self) -> BehaviourStatus:
        """Status of behaviour."""
        return self._status

    @status.setter
    def status(self, status: BehaviourStatus) -> None:
        self._status = status

    @property
    def name(self) -> str:
        """The name of behaviour."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def data_store(self) -> Dict[str, Any]:
        """Data store of the behaviour."""
        return self._data_store

    @data_store.setter
    def data_store(self, data_store: Dict[str, Any]) -> None:
        self._data_store = data_store

    @abstractmethod
    def action(self) -> None:
        """Set operations to be performed by the behavior.

        Raises:
            TypeError: To be implemented...
        """

    def block(self, millisecond: int = 0) -> None:
        """Blocks this behaviour.

        Args:
            millisecond (int, optional): Time before the behaviour restarts.
                Defaults to 0.
        """
        self._status = BehaviourStatus.BLOCKED
        if millisecond:
            self._date_to_restart = datetime.now() + timedelta(
                milliseconds=millisecond
            )
        else:
            self._date_to_restart = None

    @abstractmethod
    def done(self) -> bool:
        """Get the behaviour has completed its execution.

        Returns:
            bool: True if the behaviour has completed its execution.

        Raises:
            TypeError: To be implemented...
        """

    def is_runnable(self) -> bool:
        """Check if behaviour is runnable (status not blocked).

        Returns:
            bool: True if status is not blocked.
        """
        if (
            self._status == BehaviourStatus.BLOCKED
            and self._date_to_restart
            and self._date_to_restart <= datetime.now()
        ):
            self.restart()

        return self._status != BehaviourStatus.BLOCKED

    def _on_start(self) -> None:
        """Save initial state of behaviour and call on_start method."""
        self._save_init_state()
        self._status = BehaviourStatus.STARTED
        self.on_start()

    def on_start(self) -> None:
        """Call before action method."""

    def on_end(self) -> int:
        """Call after done method.

        Returns:
            int: Code to finish behaviour. Default to 0.
        """
        return 0

    def reset(self) -> None:
        """Restores behaviour initial state."""
        if self._init_state:
            self.__dict__ = self._init_state
        self._save_init_state()

    def restart(self) -> None:
        """Restarts a blocked behaviour."""
        self._status = BehaviourStatus.STARTED
        self._date_to_restart = None

    def run(self) -> Optional[int]:
        """Run the behaviour.

        Returns:
            Optional[int]: The return of on_end method or None if not done.
        """
        if self._status == BehaviourStatus.NOT_STARTED:
            self._on_start()
        if self._status == BehaviourStatus.STOPPED:
            return self.on_end()
        if self.is_runnable():
            self.action()
            if self.done():
                return self.on_end()
        return None

    def _save_init_state(self) -> None:
        """Save the behaviour initial state."""
        self._init_state = self.__dict__.copy()
