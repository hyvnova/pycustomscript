if __name__ != "__main__":
    print("THIS FILE SHOULD NOT BE IMPORTED, IS SUPPOSED TO BE RUNNED DIRECTLY")        
    exit(0)


import argparse

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
    parse_config_file()    
    
    # file that'd be ran
    entry_files = args.filename
    prepare: bool = get_from_config_file("prepare")
    
    
    if not entry_files:
        entry_files = get_from_config_file("run")
    
    if isinstance(entry_files, str):
        entry_files = [entry_files]
        
    for file in entry_files:
        
        if prepare:
            run(file)
            
        else:
            system(f"python {Path(file).absolute()}")