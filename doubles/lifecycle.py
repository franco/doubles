from threading import local
from contextlib import contextmanager

from doubles.space import Space


_thread_local_data = local()


def current_space():
    """
    An accessor for the current thread's active ``Space``.

    :return: The active ``Space``.
    :rtype: Space
    """

    if not hasattr(_thread_local_data, 'current_space'):
        _thread_local_data.current_space = Space()

    return _thread_local_data.current_space


def teardown():
    """Tears down the current Doubles environment. Must be called after each test case."""
    if hasattr(_thread_local_data, 'current_space'):
        _thread_local_data.current_space.teardown()
        del _thread_local_data.current_space


def verify():
    """
    Verifies any mocks that have been created during the test run. Must be called after each
    test case, but before teardown.
    """

    if hasattr(_thread_local_data, 'current_space'):
        _thread_local_data.current_space.verify()


@contextmanager
def no_builtin_verification():
    """
    While inside this context we will ignore errors raised while verifying the
    arguments of builtins.

    Note: It is impossible to verify the expected arugments of built in functions
    """
    current_space().skip_builtin_verification = True
    yield
    current_space().skip_builtin_verification = False


def ignore_builtin_verification():
    """
    Check if we ignoring builtin argument verification errors.

    :return: True if we are ignoring errors.
    :rtype: bool
    """
    return not current_space().skip_builtin_verification
