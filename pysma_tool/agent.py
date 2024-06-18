"""Agent module"""

from typing import List
from threading import Thread
from abc import ABC, abstractmethod

from .behaviours.behaviour import Behaviour


class Agent(ABC, Thread):
    def __init__(self, agent_id: str) -> None:
        super().__init__()
        self._behaviours: List[Behaviour] = []
        self._agent_id: str = agent_id
        self._agent_delete: bool = False
        # self._data_store: Dict[str, Any] = {}

    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError

    def add_behaviour(self, behaviour: Behaviour) -> None:
        behaviour.agent = self
        self._behaviours.append(behaviour)

    def do_delete(self) -> None:
        self._agent_delete = True

    def take_down(self) -> None:
        pass

    def run(self) -> None:
        self.setup()
        while not self._agent_delete:
            # on_end_result: Optional[int] = behaviour.run()
            behaviours_to_remove: List[Behaviour] = [
                behaviour
                for behaviour in self._behaviours
                if behaviour.run() is not None
            ]
            for behaviour in behaviours_to_remove:
                self._behaviours.remove(behaviour)
            if not self._behaviours:
                self.do_delete()
        self.take_down()
