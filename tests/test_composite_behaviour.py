import pytest

from pysma_tool.behaviours.composite_behaviour import CompositeBehaviour
from pysma_tool.exceptions.exceptions import BehaviourException
from pysma_tool.behaviours.one_shot_behaviour import OneShotBehaviour


class MyBehaviour(CompositeBehaviour):
    pass


class MyTestBehaviour(OneShotBehaviour):
    def action(self) -> None:
        self._data_store["toto"] = 55
        if self._parent:
            self._parent.data_store["counter"] = 42
    

@pytest.fixture
def my_behaviour() -> MyBehaviour:
    return MyBehaviour()


@pytest.fixture
def my_test_behaviour() -> MyTestBehaviour:
    return MyTestBehaviour()


class TestAddSubBehaviourBehaviour:
    def test_add_sub_behaviour_with_exception(
        self, my_behaviour: MyBehaviour
    ) -> None:
        with pytest.raises(BehaviourException):
            my_behaviour.add_sub_behaviour("toto", "toto")

    def test_add_sub_behaviour_with_other_exception(
        self, my_behaviour: MyBehaviour, my_test_behaviour: MyTestBehaviour
    ) -> None:
        my_behaviour.add_sub_behaviour(my_test_behaviour, "toto")
        with pytest.raises(BehaviourException):
            my_behaviour.add_sub_behaviour(my_test_behaviour, "toto")

    def test_add_sub_behaviour_parent(
        self, my_behaviour: MyBehaviour, my_test_behaviour: MyTestBehaviour
    ) -> None:
        my_behaviour.add_sub_behaviour(my_test_behaviour, "toto")
        assert my_behaviour.children_graph.get_node(
            "toto"
        ).node_content.parent == my_behaviour

    def test_add_sub_behaviour(
        self, my_behaviour: MyBehaviour, my_test_behaviour: MyTestBehaviour
    ) -> None:
        my_behaviour.add_sub_behaviour(my_test_behaviour, "toto")
        my_behaviour.children_graph.get_node(
            "toto"
        ).node_content.action()
        assert my_behaviour.children_graph.get_node(
            "toto"
        ).node_content.data_store["toto"] == 55 and my_behaviour.data_store[
            "counter"
        ] == 42
