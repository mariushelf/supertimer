import time

import pytest
from supertimer import timer


def test_timer():
    with timer("Test", print=True):
        time.sleep(0.01)


def test_timer_with_exception():
    with pytest.raises(ValueError):
        with timer("Raise exception", print=True):
            raise ValueError("oopsie")
