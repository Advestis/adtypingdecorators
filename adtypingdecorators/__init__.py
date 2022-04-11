"""
Python decorators allowing to check and/or enforce types in functions' arguments based on typing hints.


>>> import numpy as np
>>> import pandas as pd
>>> from adtypingdecorators import typing_raise, typing_convert, typing_warn, typing_custom
>>>
>>>
>>> def to_array(a: int):
>>>     return np.array([a, 2 * a])
>>>
>>>
>>> def to_array_2(a: int):
>>>     return np.array([a, 3 * a])
>>>
>>>
>>> @typing_raise
>>> def f_raise(a: int):
>>>     return a + 1
>>>
>>>
>>> @typing_convert
>>> def f_convert(a: int):
>>>     return a + 1
>>>
>>>
>>> @typing_warn
>>> def f_warn(a: int):
>>>     return a + 1
>>>
>>>
>>> @typing_custom(
>>>     convertors={int: to_array, "b": to_array_2},
>>>     exclude=["c", pd.DataFrame]
>>> )
>>> def f_custom(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray):
>>>     return a + 1, b + 1, c + 1, d + 1
>>>
>>>
>>> f_raise(1)
2
>>> # noinspection PyTypeChecker
>>> f_raise(1.5)  # Raises
TypeError
>>> # noinspection PyTypeChecker
>>> f_convert(1.5)
2
>>> # noinspection PyTypeChecker
>>> f_convert("foo")
ValueError
>>> # noinspection PyTypeChecker
>>> f_warn(1.5)  # Returns 2.5, and warns
2.5
>>> # noinspection PyTypeChecker
>>> a_, b_, c_, d_ = f_custom(1, 2, 3, pd.DataFrame([4]))
np.array([2, 3]), np.array([3, 7]), 4, pd.DataFrame([5])
"""


from .decorators import typing_raise, typing_custom, typing_convert, typing_warn
from .checker import IterableNotStr
