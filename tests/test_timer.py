import time

from supertimer import timer


def test_timer():
    with timer("Test", print=True):
        time.sleep(0.01)
