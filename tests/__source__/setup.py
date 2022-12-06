
from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        "/workspaces/PyCustomScript/tests/__source__/cython_build/funcs.pyx",
        language_level = "3",
    )
)
