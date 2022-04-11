from pathlib import Path
import sys
import versioneer

from setuptools import setup

cmdclass = versioneer.get_cmdclass()
sdist_class = cmdclass["sdist"]

workdir = Path(__file__).parent

name = "adtypingdecorators"
author = "Advestis"
author_email = "pythondev@advestis.com"
description = "A Python decorators allowing to check and/or enforce types in functions' arguments based on typing hints"
url = f"https://github.com/Advestis/{name}"

if __name__ == "__main__":

    version = ".".join(versioneer.get_version().split(".")[0:2]).replace("+", ".")
    setup(
        version=versioneer.get_version(),
        cmdclass=cmdclass,
    )
