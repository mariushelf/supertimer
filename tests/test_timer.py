import logging
import re
import time
import timeit

import pytest

from supertimer import timer
from supertimer.timer import debug_timer, info_timer, print_timer


@pytest.mark.parametrize(
    "Timer, kwargs",
    [
        (timer, {"print": True, "log": False}),
        (print_timer, {}),
    ],
)
def test_timer__print(Timer, kwargs, capsys, caplog):
    with caplog.at_level(logging.DEBUG):
        with Timer("Test", **kwargs):
            time.sleep(0.01)
    cap = capsys.readouterr()
    output = cap.out
    error = cap.err

    assert re.match(
        r"Test starting at \d+-\d+-\d+ \d+:\d+:\d+\.\d+.\nTest finished successfully at \d+-\d+-\d+ \d+:\d+:\d+\.\d+ after \d+:\d+:\d+\.\d+\.\n",
        output,
    )

    assert error == ""
    assert len(caplog.records) == 0, "there should be no log records"


@pytest.mark.parametrize(
    "Timer,kwargs,level",
    [
        (timer, {}, logging.DEBUG),
        (timer, dict(loglevel=logging.DEBUG), logging.DEBUG),
        (debug_timer, {}, logging.DEBUG),
        (info_timer, {}, logging.INFO),
    ],
)
def test_timer__logging(Timer, kwargs, level, capsys, caplog):
    with caplog.at_level(level):
        with Timer("Test", **kwargs):
            time.sleep(0.001)

    cap = capsys.readouterr()
    output = cap.out

    assert output == ""

    records = caplog.records
    assert len(records) == 2
    assert records[0].levelno == level, "logging at wrong loglevel"
    assert re.match(
        r"Test starting at \d+-\d+-\d+ \d+:\d+:\d+\.\d+.",
        records[0].msg,
    )
    assert re.match(
        r"Test finished successfully at \d+-\d+-\d+ \d+:\d+:\d+\.\d+ after \d+:\d+:\d+\.\d+\.",
        records[1].msg,
    )


def test_timer_with_exception():
    with pytest.raises(ValueError):
        with timer("Raise exception", print=True):
            raise ValueError("oopsie")


def test_print_timer():
    t = print_timer("Test")
    assert t.print == True
    assert t.log == False


def test_debug_timer():
    t = debug_timer("Test")
    assert t.print == False
    assert t.loglevel == logging.DEBUG


def test_info_timer():
    t = info_timer("Test")
    assert t.print == False
    assert t.loglevel == logging.INFO


def test_timer_func(capsys):
    with print_timer("Test", timer_func=timeit.default_timer):
        time.sleep(0.001)

    cap = capsys.readouterr()
    output = cap.out
    error = cap.err

    assert re.match(
        r"Test starting at \d+\.\d+.\nTest finished successfully at \d+.\d+ after \d+\.\d+\.\n",
        output,
    )

    assert error == ""


def test_decorator(capsys):
    @print_timer("Test")
    def sleep_a_bit():
        time.sleep(0.001)

    sleep_a_bit()

    cap = capsys.readouterr()
    output = cap.out
    error = cap.err

    assert re.match(
        r"Test starting at \d+-\d+-\d+ \d+:\d+:\d+\.\d+.\nTest finished successfully at \d+-\d+-\d+ \d+:\d+:\d+\.\d+ after \d+:\d+:\d+\.\d+\.\n",
        output,
    )

    assert error == ""
