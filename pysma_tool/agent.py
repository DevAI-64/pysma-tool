from typing import List, Optional
from abc import ABC, abstractclassmethod
from threading import Thread

from .behaviours.behaviour import Behaviour


class Agent(ABC, Thread):

    def __init__(self, id: str) -> None:
        super().__init__()
        self._behaviours: List[Behaviour] = []
        self._id: str = id
        self._delete: bool = False

    @abstractclassmethod
    def setup(self) -> None:
        pass

    def add_behaviour(self, behaviour: Behaviour) -> None:
        behaviour.agent = self
        self._behaviours.append(behaviour)

    def do_delete(self) -> None:
        self._delete = True

    def take_down(self) -> None:
        pass

    def run_behaviour(self, behaviour: Behaviour) -> Optional[Behaviour]:
        if not behaviour.already_start:
            behaviour.on_start()
            behaviour.already_start = True
        behaviour.action()
        if behaviour.done():
            behaviour.on_end()
            return behaviour

    def run(self) -> None:
        self.setup()
        while not self._delete:
            behaviours_to_remove: List[Behaviour] = [
                behaviour
                for behaviour in self._behaviours
                if self.run_behaviour(behaviour)
            ]
            for behaviour in behaviours_to_remove:
                self._behaviours.remove(behaviour)
            if not self._behaviours:
                self.do_delete()
        self.take_down()
