if __name__ == "__main__":
    print(f"This file ({__name__}) should not be executed directly")
    exit(1)


from pathlib import Path
from os import system, mkdir, remove

# local
from .patterns import patterns
from .cythonizer import convert_to_cython
from .custom_builtins import set_builtins


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
    
    
    # clear __source__ dir
    if output_file.parent.name == "__source__":
        try:
            remove(output_file.parent)
        except OSError as e:
            print(f"WARNING: Could not clear {output_file.parent}\n\tError raised -> {e}")
            
        
    # create init at output file
    if not output_file.parent.exists():
        mkdir(output_file.parent)
        
        
    # file code
    raw_source = open(file, "r", encoding="utf-8").read()
    
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
    with open(output_file, "w", encoding="utf-8") as f:
        
        for pattern_handler in patterns:
            
            source = pattern_handler(source)
            
        f.write(source)
    
    return output_file.absolute()

def run(file: Path | str, __source_file: str = None, custom_builtins: bool = False, to_cython: bool = True) -> None:
    """
    Runs the code given using CustomScript Interpreter
    """
    
    if not __source_file:
        __source_file: Path = process_raw_source(file)
        
    # use custom builtins
    if custom_builtins:
        set_builtins(__source_file)
        
    # convert to cython
    if to_cython:
        convert_to_cython(__source_file)
    
    
    system(f"python {__source_file}")
              
   
    


