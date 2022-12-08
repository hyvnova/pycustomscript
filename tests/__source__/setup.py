
from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        "/workspaces/PyCustomScript/tests/__source__/funcs.py",
        language_level = "3",
        quiet = True
    )
)
