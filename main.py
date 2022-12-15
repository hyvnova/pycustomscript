

if __name__ != "__main__":
    print("THIS FILE SHOULD NOT BE IMPORTED, IS SUPPOSED TO BE RUNNED DIRECTLY")        
    exit(0)


import argparse
from typing import List

#local modules
from src.interpreter import run, system, Path
from src.parseconfig import parse_config_file, get_from_config_file



# argument parse for taking and managing command from Command line
parser = argparse.ArgumentParser(
    prog = 'main.py',
    description = 'run, prepare or manage how the PyCustomScript interpreter works',
    epilog = 'check help.md to see the list a explanation of all commands'
)


parser.add_argument(
    "action", 
    default="run", 
    
    # COMMAND LIST  ---------------------------- <!> ---------------------------------
    choices=[
        "run"
    ]
)
parser.add_argument("-f", "--filename", required=False)



# MANAGE COMMAND

args = parser.parse_args()

# RUN COMMAND
if args.action == "run":
    
    # Prepares all modules listed in the config file
    config_data = parse_config_file()    
    
    
    # if no entry files then entry files will be got from the config file, in which they could be a list
    entry_files: str | List[str] = (args.filename or get_from_config_file("run"))
    
    # if no entry files if found then raise an error
    if not entry_files:
        raise ValueError("No file was given at run command or found at config file.")
    
    if isinstance(entry_files, str):
        entry_files = [entry_files]
        
    for file in entry_files:
        run(file, custom_builtins=config_data.get("custom_builtins"), to_cython=config_data.get("to_cython"))
            