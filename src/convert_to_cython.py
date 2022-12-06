from distutils.command.build import build
from pathlib import Path
import re, os, sys
from distutils.core import setup
from Cython.Build import cythonize

def convert_to_cython(src):
    # Replace variable declarations with C types
    src = re.sub(r'(int|float|double|char|bool)\s+(\w+)', r'cdef \1 \2', src)

    # Replace function declarations with C types
    src = re.sub(r'def\s+(\w+)\((.*?)\):', r'cdef \1(\2):', src)

    return src

def create_setup_py(file: Path, build_dir: Path):
    return '''
from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        "{file}",
        language_level = "3",
    )
)
'''.format(file=file, build_dir=build_dir)


def build_cython_module(file: Path | str) -> Path:
    if isinstance(file, str): file = Path(file)
    
    src: str = open(file, "r", encoding="utf-8").read()
    
    name = file.name[:-3] 
    HERE = file.parent # where the builded module should end up
    BUILD_DIR = HERE / "cython_build" # temp files and stuff
    
    print(f"{HERE = }\n{BUILD_DIR = }")
    
    if not HERE.exists():
        os.mkdir(HERE)
        # create init file
        open(HERE / "__init__.py", "w", encoding="utf-8").write("# THIS FILE TELL PYTHON THAT THIS IS A MODULE")
    
    # if build dir doesnt exists, create it
    if not BUILD_DIR.exists():
        os.mkdir(BUILD_DIR)
    
    
    # Convert the source code to Cython
    cython_src = convert_to_cython(src)

    # Create the .pyx file
    pyx_source_path = BUILD_DIR / (name + '.pyx')
    
    with open(pyx_source_path, 'w') as f:
        f.write(cython_src)

    # Create the setup.py file
    setup_py = create_setup_py(pyx_source_path, HERE)
    
    with open(HERE / 'setup.py', 'w') as f:
        f.write(setup_py)
           

    # Build the Cython extension
    os.getcwd()
    os.system(f'python {HERE / "setup.py"} build_ext --build-lib {HERE} --build-temp {BUILD_DIR}')

    # Return the path to the compiled Cython module
    return HERE / name # file extension is not needed, because python will give priority to a .so file 

