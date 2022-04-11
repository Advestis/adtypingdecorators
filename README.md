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
from adtypingdecorators import typing_raise, typing_convert

@typing_raise
def f_raise(a: int):
    return a + 1

@typing_convert
def f_convert(a: int):
    return a + 1

f_raise(1)  # returns 2
f_raise(1.5)  # returns TypeError
f_convert(1.5)  # returns 2 (casts 1.5 to integer, so to 1, then adds 1)
```
