import pytest

from pysma_tool.behaviours.cyclic_behaviour import CyclicBehaviour



class MyBehaviour(CyclicBehaviour):
    def __init__(self) -> None:
        super().__init__()
        self._counter: int  = 0

    def action(self) -> None:
        self.data_store[f"my_key{self._counter}"] = "toto"
        self._counter += 1

    def done(self) -> bool:
        return True if self._counter == 5 else False
    

class MyBehaviourWithoutDoneOverwrite(CyclicBehaviour):
    def __init__(self) -> None:
        super().__init__()
        self._counter: int  = 0

    def action(self) -> None:
        self.data_store[f"my_key{self._counter}"] = "toto"
        self._counter += 1


@pytest.fixture
def my_behaviour() -> MyBehaviour:
    return MyBehaviour()


@pytest.fixture
def my_behaviour_without_done_overwrite() -> MyBehaviourWithoutDoneOverwrite:
    return MyBehaviourWithoutDoneOverwrite()


class TestCyclicBehaviour:
    def test_cyclic_behaviour(self, my_behaviour: MyBehaviour) -> None:
        while not my_behaviour.done():
            my_behaviour.action()

        assert my_behaviour.data_store == {
            "my_key0": "toto",
            "my_key1": "toto",
            "my_key2": "toto",
            "my_key3": "toto",
            "my_key4": "toto",
        }

    def test_done(self, my_behaviour: MyBehaviour) -> None:
        assert not my_behaviour.done()
    
    def test_done_without_overwrite(
        self,
        my_behaviour_without_done_overwrite: MyBehaviourWithoutDoneOverwrite
    ) -> None:
        assert not my_behaviour_without_done_overwrite.done()