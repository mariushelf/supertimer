import datetime as dt
import logging
from typing import Callable

module_logger = logging.getLogger(__name__)


class timer:
    """Context manager that prints and/or logs the duration of the code block.

    Parameters
    ----------
    description : str, optional
        description of the timer. Used in log messages. Default: "Timer"
    print: bool, optional
        whether to print the log messages. Default: False
    loglevel: int, optional
        loglevel of logmessages produced by the timer. If ``None``, nothing is logged
        (useful if `print` is True). default: ``logging.DEBUG``.
    logger : logging.Logger, optional
        which logger to use. Default: a logger with the name of this module
    timer_func : Callable, optional
        function which return the current time at begin and end of the job.
        Must return something that supports difference when called without an argument.
        Default is ``datetime.datetime.now``. Since it's difference is a
        ``datetime.timedelta`` the output is nicely formatted.
        For an output in seconds ``timeit.default_timer`` could be a good choice.


    Examples
    --------
    >>> with timer("sleep a while", loglevel=logger.INFO):
    ...    time.sleep(2)
    """

    def __init__(
        self,
        description: str = None,
        print: bool = False,
        loglevel: int = logging.DEBUG,
        logger: logging.Logger = None,
        timer_func: Callable = dt.datetime.now,
    ):
        self.description = description or "Timer"
        self.print = print
        self.loglevel = loglevel
        self.logger = logger or module_logger
        self.timer_func = timer_func

    def __enter__(self):
        self.start = self.timer_func()
        msg = f"{self.description} starting at {self.start}"
        if self.print:
            print(msg)
        if self.loglevel is not None:
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
        if self.loglevel is not None:
            self.logger.log(self.loglevel, msg)


class print_timer(timer):
    """ Convenience class which prints timings to stdout, but does not log. """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, print=True, loglevel=None, **kwargs)


class debug_timer(timer):
    """ Convenience class for a timer with loglevel DEBUG """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, loglevel=logging.DEBUG, **kwargs)


class info_timer(timer):
    """ Convenience class for a timer with loglevel INFO """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, loglevel=logging.INFO, **kwargs)
