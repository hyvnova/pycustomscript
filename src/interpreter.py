from pathlib import Path
from importlib import import_module
from importlib.machinery import SourceFileLoader
from os import system, mkdir

# local
from .patterns import patterns


def process_raw_source(
    file: Path | str, 
    output_file: str = "__source__/{filename}"
) ->  Path:
    """
    Takes the given `raw_source` and proecesses it to created a Python runable source file.
    Returns the source absolute path
    """
    if isinstance(file, str): 
        if not file.endswith(".py"):
            file += ".py"
            
        file = Path(file).absolute()

    # format output file name
    output_file: Path = file.parent / output_file.format(filename=Path(file).name)
    
    # file code
    raw_source = open(file, "r").read()
    
    # output source
    source = ""

    # clean lines
    for line in raw_source.split("\n"):

        # skip empty lines or comments
        if not line.strip() or line.startswith("#"):
            continue

        # remove commet
        if "#" in line:
            line = line.split("#")[0]

        source += line + "\n"

    # create __source__ folder if not exists
    if not output_file.parent.exists():
        mkdir(output_file.parent) 

    # apply patterns and save source
    with open(output_file, "w") as f:
        
        for pattern_handler in patterns:
            
            source = pattern_handler(source)
            
        f.write(source)
    
    return output_file.absolute()

def run(file: Path | str, __source_file: str = None) -> None:
    """
    Runs the code given using CustomScript Interpreter
    """
    if not __source_file:
        __source_file = process_raw_source(file)
    
    system(f"py {__source_file}")
          
def import_from_path(module_name: str, path: Path) -> str:
    # should convert the pass to a python import pass and import that path
    return SourceFileLoader(module_name, path).load_module()


              
def prepare_module(file: str):
    """
    Creates CustomScript `module` off the given `file`
    """
    source_file = process_raw_source(file)
    return import_module(source_file.name[:-3])


