import datetime as dt
import logging
from contextlib import ContextDecorator
from typing import Callable

module_logger = logging.getLogger("supertimer")


class timer(ContextDecorator):
    """Context manager that prints and/or logs the duration of the code block.

    Parameters
    ----------
    description : str, optional
        description of the timer. Used in log messages. Default: "Timer"
    print: bool, optional
        whether to print the log messages. Default: use ``default_print``
    log: bool, optional
        whether to print the log messages. Default: use ``default_log``
    loglevel: int, optional
        loglevel of logmessages produced by the timer. If ``None``, nothing is logged
        (useful if `print` is True). default: ``logging.DEBUG``.
    logger : logging.Logger, optional
        which logger to use. Default: use ``default_logger``, which itself defaults
        to a logger named ``supertimer``.
    timer_func : Callable, optional
        function which return the current time at begin and end of the job.
        Must return something that supports difference when called without an argument.
        Default: ``default_timer_func``, which itself defaults to
        ``datetime.datetime.now``. Since it's difference is a
        ``datetime.timedelta`` the output is nicely formatted.
        For an output in seconds ``timeit.default_timer`` could be a good choice.


    Examples
    --------
    >>> with timer("sleep a while", loglevel=logger.INFO):
    ...    time.sleep(2)
    """

    default_logger = module_logger
    default_loglevel = logging.DEBUG
    default_print = False
    default_log = True
    default_timer_func: Callable = dt.datetime.now

    def __init__(
        self,
        description: str = None,
        print: bool = None,
        log: bool = None,
        loglevel: int = None,
        logger: logging.Logger = None,
        timer_func: Callable = None,
    ):
        self.description = description or "Timer"
        self.print = print if print is not None else self.default_print
        self.log = log if log is not None else self.default_log
        self.loglevel = loglevel if loglevel is not None else self.default_loglevel
        self.logger = logger or self.default_logger
        self.timer_func = timer_func or self.default_timer_func

    def __enter__(self):
        self.start = self.timer_func()
        msg = f"{self.description} starting at {self.start}"
        if self.print:
            print(msg)
        if self.log:
            self.logger.log(self.loglevel, msg)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = self.timer_func()
        duration = self.end - self.start
        if exc_type:
            success_msg = f"with {exc_type.__name__}('{exc_val}')"
        else:
            success_msg = "successfully"
        msg = (
            f"{self.description} finished {success_msg} at {self.end} after {duration}."
        )
        if self.print:
            print(msg)
        if self.log:
            self.logger.log(self.loglevel, msg)


class print_timer(timer):
    """ Convenience class which prints timings to stdout, but does not log. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, print=True, log=False, **kwargs)


class debug_timer(timer):
    """ Convenience class for a timer with loglevel DEBUG """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, loglevel=logging.DEBUG, **kwargs)


class info_timer(timer):
    """ Convenience class for a timer with loglevel INFO """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, loglevel=logging.INFO, **kwargs)
