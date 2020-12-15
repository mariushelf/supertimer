# supertimer

Contextmanager to print or log execution time of code blocks

Original url: https://github.com/mariushelf/supertimer


# Etymology

This package provides a timer. But the name `timer` was already taken.
So I needed a new name. Inspired by my recently freshly flamed up
love for the good old Super Nintendo, I thought that this timer could
as well be *super*.


# Usage

## Use as a context manager

To log the duration of a code block:
```python
from supertimer import timer
import time

with timer("Sleeping a bit"):
    time.sleep(2)
```
This will log:
```
Sleeping a bit starting at 2020-12-14 18:34:54.403371
Sleeping a bit finished successfully at 2020-12-14 18:34:56.404208 after 0:00:02.000837.
```

## Use as a decorator

```python
from supertimer import timer
import time

@timer("Sleeping a bit")
def sleep_a_bit():
    time.sleep(2)

sleep_a_bit()
```

This will log the same message as the context manager each time
the decorated function is called:
```
Sleeping a bit starting at 2020-12-14 18:34:54.403371
Sleeping a bit finished successfully at 2020-12-14 18:34:56.404208 after 0:00:02.000837.
```


## Configuring the output method

By default, the output is logged at loglevel `DEBUG`.

The loglevel can be changed with the `loglevel` parameter. Printing to `stdout` can be
activated by setting the `print` parameter to `True`. Logging can be disabled by
setting `log` to `False`:

```python
with timer(loglevel=logging.INFO):
    # logging at loglevel INFO, no printing
    ...
    
with timer(print=True, log=False):
    # just printing, no logging
    ...
```

## Changing the logger

The logger can be configured:
```python
import logging

logger = logging.getLogger("my.custom.logger")
with timer(logger=logger):
    do_something()
```

If no logger is provided, a logger named `supertimer` is used.


## Convenience classes

There are convenience classes which are preconfigured for a certain loglevel or
just printing:
* `print_timer`
* `debug_timer`
* `info_timer`

## Configuring defaults

All constructor arguments have a `default_.*` class attribute counterpart which
specify defaults in case the arguments are omitted.

For example, to change the default loglevel to `WARNING` one could do:

```python
timer.default_loglevel = logging.WARNING
with timer("Sleep warning"):
    # log timings with loglevel `WARNING`
    time.sleep(2)
    
with timer("Sleep debug", loglevel=logging.DEBUG):
    # log timings with loglevel `DEBUG`
    time.sleep(2)
```


# How time is measured

By default, the start and end time are taken with `datetime.dateime.now`. The duration
is calculated as the difference of start and end time, resulting in a 
`datetime.timedelta` object.

The timer function can be overridden:
```python
import timeit

with timer(timer_func=timeit.default_timer):
    ...
```
The `timer_func` parameter expects a callable that returns a value which supports the
`minus` operation when called without an argument.


# License

[MIT](LICENSE)


# Changelog

## 0.4.0
* timer can now be used as a decorator
* global default configuration
* additional `log` parameter
* documentation
* change name of default logger to `supertimer`

## 0.3.0
* convenience classes `print_timer`, `debug_timer` and `info_timer`
* make timer function configurable

## 0.2.0
* mention success or error after execution

## 0.1.0
* First release


# Author

Marius Helf ([helfsmarius@gmail.com](mailto:helfsmarius@gmail.com))
