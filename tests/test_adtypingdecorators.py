import numpy as np
import pandas as pd
from adtypingdecorators import typing_raise, typing_convert, typing_warn, typing_custom
import pytest


def to_array(a: int):
    return np.array([a, 2 * a])


def to_array_2(a: int):
    return np.array([a, 3 * a])


@typing_raise
def f_raise(a: int):
    return a + 1


@typing_convert
def f_convert(a: int):
    return a + 1


@typing_warn
def f_warn(a: int):
    return a + 1


@typing_custom(
    convertors={int: to_array, "b": to_array_2},
    exclude=["c", pd.DataFrame]
)
def f_custom(a: np.ndarray, b: np.ndarray, c: np.ndarray, d: np.ndarray):
    return a + 1, b + 1, c + 1, d + 1


# noinspection PyTypeChecker
def test_raise():
    assert f_raise(1) == 2
    with pytest.raises(TypeError):
        f_raise(1.5)


# noinspection PyTypeChecker
def test_convert():
    assert f_convert(1.5) == 2
    with pytest.raises(ValueError):
        f_convert("chien")


# noinspection PyTypeChecker
@pytest.mark.filterwarnings("error")
def test_warning():
    with pytest.raises(Warning):
        f_warn(1.5)


# noinspection PyTypeChecker
def test_warning_2():
    assert f_warn(1.5) == 2.5


# noinspection PyTypeChecker
def test_custom():
    a, b, c, d = f_custom(1, 2, 3, pd.DataFrame([4]))
    np.testing.assert_array_equal(a, np.array([2, 3]))
    np.testing.assert_array_equal(b, np.array([3, 7]))
    assert c == 4
    pd.testing.assert_frame_equal(d, pd.DataFrame([5]))
