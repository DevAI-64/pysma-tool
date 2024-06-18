from datetime import datetime
from typing import Any, Dict, Optional
import pytest

from pysma_tool.behaviours.behaviour import Behaviour
from pysma_tool.behaviours.behaviour_status import BehaviourStatus



class MyBehaviour(Behaviour):
    def action(self) -> None:
        self.data_store["my_key"] = "toto"

    def done(self) -> bool:
        return True
    
    def on_start(self) -> None:
        self.data_store["on_start"] = "ok"


@pytest.fixture
def my_behaviour() -> MyBehaviour:
    return MyBehaviour()


class TestBehaviourAction:
    def test_action_with_raise(self) -> None:
        with pytest.raises(TypeError):
            Behaviour()

    def test_action(self, my_behaviour: MyBehaviour) -> None:
        my_behaviour.action()
        assert my_behaviour.data_store.get("my_key", "") == "toto"


class TestBehaviourBlock:
    def test_block_with_millisecond(self, my_behaviour: MyBehaviour) -> None:
        my_behaviour.block(5000)
        assert (
            my_behaviour.status == BehaviourStatus.BLOCKED and
            my_behaviour._date_to_restart
        )

    def test_block_without_millisecond(
        self, my_behaviour: MyBehaviour
    ) -> None:
        my_behaviour.block()
        assert (
            my_behaviour.status == BehaviourStatus.BLOCKED and
            not my_behaviour._date_to_restart
        )


class TestBehaviourDone:
    def test_done(self, my_behaviour: MyBehaviour) -> None:
        assert my_behaviour.done()


class TestBehaviourIsRunnable:
    def test_is_runnable_with_status_blocked(
        self, my_behaviour: MyBehaviour
    ) -> None:
        my_behaviour.status = BehaviourStatus.BLOCKED
        assert not my_behaviour.is_runnable()

    def test_is_runnable_with_restart(
        self, my_behaviour: MyBehaviour
    ) -> None:
        my_behaviour.status = BehaviourStatus.BLOCKED
        my_behaviour._date_to_restart = datetime.now()
        assert my_behaviour.is_runnable()

    def test_is_runnable_with_status_not_blocked(
        self, my_behaviour: MyBehaviour
    ) -> None:
        my_behaviour.status = BehaviourStatus.STARTED
        assert my_behaviour.is_runnable()


class TestBehaviourOnStart:
    def test_on_start(
        self, my_behaviour: MyBehaviour
    ) -> None:
        my_behaviour._on_start()
        assert (
            my_behaviour.status == BehaviourStatus.STARTED and
            my_behaviour.data_store.get("on_start", "") == "ok"
        )


class TestBehaviourOnEnd:
    def test_on_end(
        self, my_behaviour: MyBehaviour
    ) -> None:
        assert my_behaviour.on_end() == 0


class TestBehaviourReset:
    def test_reset(
        self, my_behaviour: MyBehaviour
    ) -> None:
        init_state: Dict[str, Any] = my_behaviour.__dict__.copy()
        my_behaviour._on_start()
        my_behaviour.reset()
        assert (
            my_behaviour._init_state == init_state and
            my_behaviour.status == BehaviourStatus.NOT_STARTED
        )


class TestBehaviourRestart:
    def test_restart(
        self, my_behaviour: MyBehaviour
    ) -> None:
        my_behaviour.status = BehaviourStatus.BLOCKED
        my_behaviour._date_to_restart = datetime.now()
        my_behaviour.restart()
        assert (
            not my_behaviour._date_to_restart and
            my_behaviour.status == BehaviourStatus.STARTED
        )


class TestBehaviourRun:
    def test_run_with_status_not_started(
        self, my_behaviour: MyBehaviour
    ) -> None:
        result: Optional[int] = my_behaviour.run()
        assert (
            my_behaviour.data_store.get("on_start") == "ok" and
            my_behaviour.status == BehaviourStatus.STARTED and
            my_behaviour.data_store.get("my_key") == "toto" and
            result == 0
        )

    def test_run_with_status_blocked(
        self, my_behaviour: MyBehaviour
    ) -> None:
        my_behaviour.status = BehaviourStatus.BLOCKED
        assert my_behaviour.run() is None

    def test_run_with_status_stopped(
        self, my_behaviour: MyBehaviour
    ) -> None:
        my_behaviour.status = BehaviourStatus.STOPPED
        assert my_behaviour.run() == 0