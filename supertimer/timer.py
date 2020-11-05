import datetime as dt
import logging

module_logger = logging.getLogger(__name__)


class timer:
    """ Context manager that prints and/or logs the duration of the code block.

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

    Examples
    --------
    with timer("sleep a while", loglevel=logger.INFO):
        time.sleep(2)
    """

    def __init__(
        self,
        description: str = None,
        print: bool = False,
        loglevel: int = logging.DEBUG,
        logger: logging.Logger = None,
    ):
        self.description = description or "Timer"
        self.print = print
        self.loglevel = loglevel
        self.logger = logger or module_logger

    def __enter__(self):
        self.start = dt.datetime.now()
        msg = f"{self.description} starting at {self.start}"
        if self.print:
            print(msg)
        if self.loglevel is not None:
            self.logger.log(self.loglevel, msg)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = dt.datetime.now()
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
