"""Waker behaviour module"""

from datetime import datetime, timedelta
from abc import abstractmethod
from typing import Optional

from .behaviour_status import BehaviourStatus
from .one_shot_behaviour import OneShotBehaviour


class WakerBehaviour(OneShotBehaviour):
    """Define WakerBehaviour class inherits to OneShotBehaviour."""

    def __init__(
        self, wake_up_date: Optional[datetime] = None, timeout: int = 0
    ) -> None:
        """Instantiate WakerBehaviour class.

        Args:
            wake_up_date (Optional[datetime], optional): Date when the task
                must be executed. Defaults to None.
            timeout (int, optional): Number of milliseconds after which the
                task must be executed. Defaults to 0.
        """
        super().__init__()
        self.reset(wake_up_date=wake_up_date, timeout=timeout)

    def action(self) -> None:
        """Call on_wake method."""
        self.on_wake()

    def _on_start(self) -> None:
        """Save initial state of behaviour and call on_start method."""
        self._save_init_state()
        self._status = BehaviourStatus.BLOCKED
        self.on_start()

    @abstractmethod
    def on_wake(self) -> None:
        """Set operations to be performed by the behavior.

        Raises:
            NotImplementedError: To be implemented...
        """

    def reset(
        self, wake_up_date: Optional[datetime] = None, timeout: int = 0
    ) -> None:
        """Restores behaviour initial state.

        Args:
            wake_up_date (Optional[datetime], optional): Date when the task
                must be executed. Defaults to None.
            timeout (int, optional): Number of milliseconds after which the
                task must be executed. Defaults to 0.
        """
        super().reset()
        if wake_up_date:
            self._date_to_restart = wake_up_date
        if self._date_to_restart and timeout:
            self._date_to_restart += timedelta(milliseconds=timeout)
        if not self._date_to_restart and timeout:
            self._date_to_restart = datetime.now() + timedelta(
                milliseconds=timeout
            )

    def stop(self) -> None:
        """Stop the behaviour without call on_wake method."""
        self._status = BehaviourStatus.STOPPED
