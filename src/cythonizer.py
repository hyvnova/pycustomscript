from pathlib import Path
import os


def create_setup_py(file: Path):
    return '''
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        r"{file}",
        language_level = "3",
        quiet = True
    )
)
'''.format(file=file)


def build_cython_module(file: Path | str, quiet: bool = False) -> Path:
    """
    Builds the Cython module off the given `file`. Also Creates a `setup.py` and other required c files to build the module
    - `file` : File which the cython module will be mode of.
    -  `quiet` : If `True` warnings won't be printed (Default: `False`)
    """
    if isinstance(file, str): file = Path(file)
        
    name = file.name[:-3] 
    HERE = file.parent # where the builded module should end up; __source__ dir
    BUILD_DIR = HERE / "cython_build" # temp files and stuff
    
    # Clear and create source module dir
    try:
        os.remove(BUILD_DIR)
        
    except OSError as e:
        
        if not quiet:
            print(f"WARNING: Could not clear {BUILD_DIR}\n\tError raised -> {e}\n")

    # if build dir doesnt exists, create it
    if not BUILD_DIR.exists():
        os.mkdir(BUILD_DIR)
    
    # Create the setup.py file
    with open(HERE / 'setup.py', 'w') as f:
        f.write(
            create_setup_py(file)
        )
           
    # Build the Cython extension
    os.system(f'python {HERE / "setup.py"} build_ext --build-lib {HERE.parent} --build-temp cython_build')

    # Return the path to the compiled Cython module
    return HERE / name # file extension is not needed, because python will give priority to a .so file 

