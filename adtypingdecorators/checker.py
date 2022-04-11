from typing import Iterable, List, Dict, Union, Tuple
import warnings
import logging

import numpy as np

logger = logging.getLogger(__name__)


class IterableNotStr:
    """A class that can be used as typing hint.

    Specifies that the variable is expected to be an iterable (list, dict, tuple...) but NOT a string.
    """

    pass


def list_intersection(lst1: Iterable, lst2: Iterable) -> List:
    """lst1 INTER lst2.

    mathematical intersection between lst1 and lst2

    Parameters
    ----------
    lst1 : list
    lst2 : list

    Returns
    -------
    List
        list of elements which are in lst1 and lst2

    See Also
    --------
    https://stackoverflow.com/questions/3697432/how-to-find-list-intersection

    Examples
    --------
    >>> list_intersection([1,5,6], [8,2,7,6,2,1,5])
    [1, 5, 6]
    >>> list_intersection([1,2,3,4,5], [1,3,5,6])
    [1, 3, 5]
    >>> list_intersection(["c", "a"], ["b"])
    []
    >>> list_intersection(["c", "a"], ["c", "b"]) == ["c"]
    True
    """
    return list(set(lst1) & set(lst2))


class FunctionArgumentsCheck(object):
    """Checks if arguments match specified types.

    Checks if the non-ignored arguments types match the function typing hints.
    If not, warns, raises an error or tries to produce valid argument types using __annotations__ and the convertors
    dict.

    Warns
    -----
    Depending on 'warn_only' and 'try_convert', will warn when types do not match typing hints.

    Raises
    ------
    TypeError
        Depending on 'warn_only' and 'try_convert', will raise when types do not match typing hints.
    """

    def __init__(
        self, try_convert: bool = False, convertors: Dict = None, warn_only: bool = False, exclude: List[str] = None
    ):
        """
        Parameters
        ----------
        try_convert: bool
            Tries to convert if types do not match (default value = False)
        convertors: Dict[str: Callable[[Any], Any]]
            Customs convertions. Keys are possible types, values are the types they should be converted into.
            If not empty, will overload 'try_convert' and set it to True.
            (default value = {})
        warn_only: bool
            Don't raise, simply warn if types do not match. If 'try_convert' is True, will first attempt to convert.
            (default value = False)
        exclude: List[str]
            Excluded argument names. Those arguments will not be checked. (default value = []).
        """
        self.try_convert = try_convert
        self.warn_only = warn_only
        if convertors:
            self.convertors = convertors
            self.try_convert = True
        else:
            self.convertors = dict()
        if exclude:
            self.exclude = exclude
        else:
            self.exclude = []

    def __call__(self, func, *args, **kwargs):
        """main check

        Parameters
        ----------
        func :
            function
        args :
            arguments
        kwargs :
            keyword arguments

        Returns
        -------
        modified arguments
        """

        args = list(args)
        typing = {
            k: v
            for k, v in func.__annotations__.items()
            if v is not None and k not in self.exclude and v not in self.exclude
        }

        varsnames = func.__code__.co_varnames
        _input = {name: val for name, val in zip(varsnames, args)}
        _input.update(kwargs)

        for name in list_intersection(_input.keys(), typing.keys()):
            args, kwargs = self.test_and_handle(name, _input[name], typing[name], varsnames, args, kwargs)
        return tuple(args), kwargs

    def test_and_handle(self, name, value, _type, varsnames, args, kwargs):
        """Checks that 'value' is of type '_type', and calls 'adtypingdecorators.checker.FunctionArgumentChecker.handle'
        if not."""
        if not self.test(value, _type):
            self.handle(name, value, _type, varsnames, args, kwargs)
        return args, kwargs

    def test(self, value, _type) -> bool:
        """Checks that 'value' is of type '_type'"""

        if type(value) in self.exclude:
            return True

        if hasattr(_type, "__origin__"):
            if _type.__origin__ == Union:
                for arg in _type.__args__:
                    if self.test(value, arg):
                        return True
                return False
            elif _type.__origin__ == list:
                return isinstance(value, list)
            elif _type.__origin__ == Dict:
                return isinstance(value, dict)
            elif _type.__origin__ == Tuple:
                return isinstance(value, tuple)
            elif _type == Iterable:
                return isinstance(value, Iterable)
            else:
                raise NotImplementedError(f"Type check for type '{_type}' is not implemented yet.")

        if _type == IterableNotStr:
            return isinstance(value, Iterable) and not isinstance(value, str)

        res = isinstance(value, _type)
        if res is False and "numpy" in str(value.__class__) and (_type == int or _type == float):
            if "numpy.int" in str(value.__class__):
                return isinstance(value, np.integer)
            elif "numpy.float" in str(value.__class__):
                return isinstance(value, float)
        return res

    # noinspection PyUnresolvedReferences
    def handle(self, name, value, _type, varsnames, args, kwargs):
        """'value''s type do not match '_type', so will attempt to convert if self.try_convert is True,
        or will warn if self.warn_only is True, or will raise TypeError."""
        _msg = f"Element '{name}' of type '{type(value)}' does not match required type '{_type}'."
        if self.try_convert:
            logger.debug(_msg)
            if name in self.convertors.keys():
                convertor = self.convertors[name]
            elif type(value) in self.convertors.keys():
                convertor = self.convertors[type(value)]
            elif hasattr(_type, "__origin__") and _type.__origin__ == Union:
                convertor = _type.__args__[0]
            else:
                convertor = _type
            if convertor == np.ndarray:
                convertor = np.array
            if name in kwargs.keys():
                kwargs[name] = convertor(kwargs[name])
            else:
                args[varsnames.index(name)] = convertor(args[varsnames.index(name)])
            return args, kwargs
        elif self.warn_only:
            warnings.warn(_msg)
        else:
            raise TypeError(_msg)
