import pytest
from datetime import datetime, timedelta

from pysma_tool.behaviours.waker_behaviour import WakerBehaviour
from pysma_tool.behaviours.waker_behaviour import WakerBehaviour
from pysma_tool.behaviours.behaviour_status import BehaviourStatus


class MyBehaviour(WakerBehaviour):
    def on_wake(self) -> None:
        self.data_store["my_key"] = "toto"


@pytest.fixture
def my_behaviour() -> MyBehaviour:
    return MyBehaviour()


class TestAction:
    def test_action(self, my_behaviour: MyBehaviour) -> None:
        my_behaviour.action()
        assert my_behaviour.data_store.get("my_key") == "toto"


class TestInstance:
    def test_instance_with_date(self) -> None:
        date: datetime = datetime(2000, 4, 14, 15, 21)
        my_behaviour: MyBehaviour = MyBehaviour(date)
        assert my_behaviour._date_to_restart == date

    def test_instance_with_time(self) -> None:
        date: datetime = datetime.now() + timedelta(
            milliseconds=1000
        )
        my_behaviour: MyBehaviour = MyBehaviour(timeout=1000)
        assert (
            my_behaviour._date_to_restart and
            my_behaviour._date_to_restart >= date
        )

    def test_instance_with_both(self) -> None:
        date: datetime = datetime(2000, 4, 14, 15, 21)
        my_behaviour: MyBehaviour = MyBehaviour(date, 1000)
        date_result: datetime = datetime(2000, 4, 14, 15, 21) + timedelta(
            milliseconds=1000
        )
        assert(
            my_behaviour._date_to_restart and
            my_behaviour._date_to_restart == date_result
        )

    def test_instance_without_both(self, my_behaviour: MyBehaviour) -> None:
        assert not my_behaviour._date_to_restart


class TestOnStart:
    def test_on_start(self, my_behaviour: MyBehaviour) -> None:
        my_behaviour._on_start()
        assert my_behaviour.status == BehaviourStatus.BLOCKED


class TestOnWake:
    def test_raise_on_wake(self) -> None:
        with pytest.raises(TypeError):
            WakerBehaviour()

    def test_on_wake(self, my_behaviour: MyBehaviour) -> None:
        my_behaviour.on_wake()
        assert my_behaviour.data_store.get("my_key") == "toto"


class TestReset:
    def test_reset_with_date(self, my_behaviour: MyBehaviour) -> None:
        date: datetime = datetime(2000, 4, 14, 15, 21)
        my_behaviour.reset(date)
        assert my_behaviour._date_to_restart == date

    def test_reset_with_time(self, my_behaviour: MyBehaviour) -> None:
        date: datetime = datetime.now() + timedelta(
            milliseconds=1000
        )
        my_behaviour._on_start()
        my_behaviour.reset(timeout=1000)
        assert (
            my_behaviour._date_to_restart and
            my_behaviour._date_to_restart >= date
        )

    def test_reset_with_both(self, my_behaviour: MyBehaviour) -> None:
        date: datetime = datetime(2000, 4, 14, 15, 21)
        my_behaviour.reset(date, 1000)
        date_result: datetime = datetime(2000, 4, 14, 15, 21) + timedelta(
            milliseconds=1000
        )
        assert(
            my_behaviour._date_to_restart and
            my_behaviour._date_to_restart == date_result
        )

    def test_reset_without_both(self, my_behaviour: MyBehaviour) -> None:
        my_behaviour._on_start()
        my_behaviour.reset()
        assert not my_behaviour._date_to_restart

    def test_reset_without_both_and_no_on_start(
        self, my_behaviour: MyBehaviour
    ) -> None:
        my_behaviour.reset()
        assert not my_behaviour._date_to_restart


class TestStop:
    def test_stop(self, my_behaviour: MyBehaviour) -> None:
        my_behaviour.stop()
        assert my_behaviour.status == BehaviourStatus.STOPPED
    