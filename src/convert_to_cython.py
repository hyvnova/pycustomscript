from distutils.command.build import build
from pathlib import Path
import os
from distutils.core import setup
from Cython.Build import cythonize

def create_setup_py(file: Path):
    return '''
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        "{file}",
        language_level = "3",
        quiet = True
    )
)
'''.format(file=file)


def build_cython_module(file: Path | str) -> Path:
    if isinstance(file, str): file = Path(file)
        
    name = file.name[:-3] 
    HERE = file.parent # where the builded module should end up; __source__ dir
    BUILD_DIR = HERE / "cython_build" # temp files and stuff
    
    # Clear and create source module dir
    try:
        os.remove(BUILD_DIR)
    except OSError as e:
        print("Error: %s : %s" % (BUILD_DIR, e.strerror))

    # create init file
    open(HERE / "__init__.py", "w", encoding="utf-8").write("# THIS FILE TELL PYTHON THAT THIS IS A MODULE")
    
    # if build dir doesnt exists, create it
    if not BUILD_DIR.exists():
        os.mkdir(BUILD_DIR)
    
    # Create the setup.py file
    setup_py = create_setup_py(file)
    
    with open(HERE / 'setup.py', 'w') as f:
        f.write(setup_py)
           

    # Build the Cython extension
    os.system(f'python {HERE / "setup.py"} build_ext --build-lib {HERE.parent} --build-temp {BUILD_DIR}')

    # Return the path to the compiled Cython module
    return HERE / name # file extension is not needed, because python will give priority to a .so file 

