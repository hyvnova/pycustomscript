from patterns import patterns
import time
from pathlib import Path
from importlib import import_module
from typing import Tuple

def process_raw_source(
    file: str | Path, 
    output_file: str = "__source_{filename}", 
    timeit: bool = False
) ->  Path:
    """
    Takes the given `raw_source` and proecesses it to created a Python runable source file.
    Returns source file name
    """
    if timeit:
        time_start = time.time()
        cpu_time_start = time.process_time()
        

    if isinstance(file, str): file = Path(file)

    # format output file name
    output_file = output_file.format(filename=Path(file).name)

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



    # apply patterns and save source
    with open(output_file, "w") as f:
        for pattern_handler in patterns:
            
            source = pattern_handler(source)
            
        f.write(source)
    
    if timeit:
        time_end = time.time()
        cpu_time_end = time.process_time()

        print(f"TIME TAKEN TO BUILD SOURCE:\n\tTOTAL TIME: {time_end - time_start}\n\tCPU TIME: {cpu_time_end - cpu_time_start}")

    return output_file

def run(file: str, __source_file: str = None) -> None:
    """
    Runs the code given using CustomScript Sintax
    """
    if not __source_file:
        __source_file = process_raw_source(file)
        
    exec(open(__source_file, "r").read())
              
def prepare_module(file: str):
    """
    Creates CustomScript `module` off the given `file`
    """
    source_file = process_raw_source(file)
    return import_module(source_file[:-3])


