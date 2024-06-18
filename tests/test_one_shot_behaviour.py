import pytest

from pysma_tool.behaviours.one_shot_behaviour import OneShotBehaviour



class MyBehaviour(OneShotBehaviour):
    def __init__(self) -> None:
        super().__init__()
        self._counter: int  = 0

    def action(self) -> None:
        self.data_store[f"my_key{self._counter}"] = "toto"
        self._counter += 1


@pytest.fixture
def my_behaviour() -> MyBehaviour:
    return MyBehaviour()


class TestOneShotBehaviour:
    def test_one_shot_behaviour(self, my_behaviour: MyBehaviour) -> None:
        my_behaviour.action()
        while not my_behaviour.done():
            my_behaviour.action()

        assert my_behaviour.data_store == {
            "my_key0": "toto"
        }

    def test_done(self, my_behaviour: MyBehaviour) -> None:
        assert my_behaviour.done()
    