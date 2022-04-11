from functools import wraps
from typing import Callable, List, Dict

import logging

from .checker import FunctionArgumentsCheck

logger = logging.getLogger(__name__)


def typing_raise(_func: Callable[[], str] = None, exclude: List[str] = None):
    """Checks if arguments match specified types

    If not, raises TypeError.

    Parameters
    ----------
    _func: Callable[[], str] = None,
        Function on which to check types.
    exclude: List[str]
        Excluded argument names. Those arguments will not be checked. (default value = []).

    Raises
    --------
    TypeError
        If types do not match

    See Also
    --------
    FunctionArgumentsCheck
    """

    def tags_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            args, kwargs = FunctionArgumentsCheck(exclude=exclude)(func, *args, **kwargs)
            ret = func(*args, **kwargs)
            return ret

        return func_wrapper

    if _func:
        return tags_decorator(_func)
    else:
        return tags_decorator


def typing_warn(_func: Callable[[], str] = None, exclude: List[str] = None):
    """Checks if arguments match specified types

    If not, warns.

    Parameters
    ----------
    _func: Callable[[], str] = None,
        Function on which to check types.
    exclude: List[str]
        Excluded argument names. Those arguments will not be checked. (default value = []).

    Warns
    --------
    If types do not match

    See Also
    --------
    FunctionArgumentsCheck
    """

    def tags_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            args, kwargs = FunctionArgumentsCheck(warn_only=True, exclude=exclude)(func, *args, **kwargs)
            ret = func(*args, **kwargs)
            return ret

        return func_wrapper

    if _func:
        return tags_decorator(_func)
    else:
        return tags_decorator


def typing_convert(_func: Callable[[], str] = None, exclude: List[str] = None):
    """Checks if arguments match specified types.

    If not, tries to convert them into the specified type.

    Parameters
    ----------
    _func: Callable[[], str] = None,
        Function on which to check types.
    exclude: List[str]
        Excluded argument names. Those arguments will not be checked. (default value = []).

    See Also
    --------
    FunctionArgumentsCheck
    """

    def tags_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            args, kwargs = FunctionArgumentsCheck(try_convert=True, exclude=exclude)(func, *args, **kwargs)
            ret = func(*args, **kwargs)
            return ret

        return func_wrapper

    if _func:
        return tags_decorator(_func)
    else:
        return tags_decorator


def typing_custom(
    _func: Callable[[], str] = None,
    try_convert: bool = False,
    convertors: Dict = None,
    warn_only: bool = False,
    exclude: List[str] = None,
):
    """Checks if arguments match specified types.

    Checks if the non-ignored arguments types match the function typing hints.
    If not, warns, raises an error or tries to produce valid argument types using __annotations__ and the convertors
    dict.

    Parameters
    ----------
    _func: Callable[[], str] = None,
        Function on which to check types.
    try_convert: bool
        Tries to convert if types do not match (default value = False)
    convertors: Dict[str: Callable[[Any], Any]]
        Customs convertions. Keys are possible types, values are the types they should be converted into.
        (default value = {})
    warn_only: bool
        Don't raise, simply warn if types do not match. If 'try_convert' is True, will first attempt to convert.
        (default value = False)
    exclude: List[str]
        Excluded argument names. Those arguments will not be checked. (default value = []).

    Warns
    -----
    Depending on 'warn_only' and 'try_convert', will warn when types do not match typing hints.

    Raises
    ------
    TypeError
        Depending on 'warn_only' and 'try_convert', will raise when types do not match typing hints.

    See Also
    --------
    FunctionArgumentsCheck
    """

    def tags_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            args, kwargs = FunctionArgumentsCheck(
                try_convert=try_convert, convertors=convertors, warn_only=warn_only, exclude=exclude
            )(func, *args, **kwargs)
            ret = func(*args, **kwargs)
            return ret

        return func_wrapper

    if _func:
        return tags_decorator(_func)
    else:
        return tags_decorator
