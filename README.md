[![doc](https://img.shields.io/badge/-Documentation-blue)](https://advestis.github.io/adtypingdecorators)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

#### Status
![Pytests](https://github.com/Advestis/adtypingdecorators/actions/workflows/pull-request.yml/badge.svg)
![push](https://github.com/Advestis/adtypingdecorators/actions/workflows/push.yml/badge.svg)

![maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![issues](https://img.shields.io/github/issues/Advestis/adtypingdecorators.svg)
![pr](https://img.shields.io/github/issues-pr/Advestis/adtypingdecorators.svg)


#### Compatibilities
![ubuntu](https://img.shields.io/badge/Ubuntu-supported--tested-success)
![unix](https://img.shields.io/badge/Other%20Unix-supported--untested-yellow)

![python](https://img.shields.io/pypi/pyversions/adtypingdecorators)


##### Contact
[![linkedin](https://img.shields.io/badge/LinkedIn-Advestis-blue)](https://www.linkedin.com/company/advestis/)
[![website](https://img.shields.io/badge/website-Advestis.com-blue)](https://www.advestis.com/)
[![mail](https://img.shields.io/badge/mail-maintainers-blue)](mailto:pythondev@advestis.com)

# AdTypingDecorators

Python decorators allowing to check and/or enforce types in functions' arguments based on typing hints.

## Installation

```bash
pip install adtypingdecorators
```

## Usage

```python
import numpy as np
import pandas as pd
from adtypingdecorators import typing_raise, typing_convert, typing_warn, typing_custom


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


f_raise(1)  # Returns 2, as expected
# noinspection PyTypeChecker
f_raise(1.5)  # Raises TypeError

# noinspection PyTypeChecker
f_convert(1.5)  # Returns 2 (converted 1.5 into 1)
# noinspection PyTypeChecker
f_convert("foo")  # Raises ValueError (while trying to convert 'foo' to interger)

# noinspection PyTypeChecker
f_warn(1.5)  # Returns 2.5, and warns

# noinspection PyTypeChecker
a_, b_, c_, d_ = f_custom(1, 2, 3, pd.DataFrame([4]))
# a_ is np.array([2, 3])
# b_ is np.array([3, 7])
# c_ is 4
# d_ is pd.DataFrame([5])
```
